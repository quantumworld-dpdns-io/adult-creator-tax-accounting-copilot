// Package consent manages GDPR / CCPA consent and DSAR requests.
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"
	"time"
)

type Consent struct {
	CreatorID  string    `json:"creator_id"`
	Purposes   []string  `json:"purposes"`
	Granted    bool      `json:"granted"`
	GrantedAt  time.Time `json:"granted_at"`
	ExpiresAt  time.Time `json:"expires_at"`
	IPHash     string    `json:"ip_hash"`
	AuditHash  string    `json:"audit_hash"`
}

type DSAR struct {
	CreatorID  string    `json:"creator_id"`
	Type       string    `json:"type"` // access, erasure, portability, restriction
	Submitted  time.Time `json:"submitted"`
	DueBy      time.Time `json:"due_by"`
	Completed  bool      `json:"completed"`
}

var (
	mu     sync.RWMutex
	consents = map[string][]Consent{}
	dsars    = map[string][]DSAR{}
)

func main() {
	addr := flag.String("addr", ":8082", "listen address")
	flag.Parse()

	mux := http.NewServeMux()
	mux.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) { w.WriteHeader(200); w.Write([]byte("ok")) })
	mux.HandleFunc("/v1/consent", consentHandler)
	mux.HandleFunc("/v1/dsar", dsarHandler)
	mux.HandleFunc("/v1/dsar/", dsarStatusHandler)
	mux.HandleFunc("/v1/gdpr/erasure", erasureHandler)

	log.Printf("consent service listening on %s", *addr)
	if err := http.ListenAndServe(*addr, mux); err != nil {
		log.Fatal(err)
	}
}

func consentHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	var c Consent
	if err := json.NewDecoder(r.Body).Decode(&c); err != nil {
		http.Error(w, "bad json", http.StatusBadRequest)
		return
	}
	c.GrantedAt = time.Now()
	c.ExpiresAt = c.GrantedAt.Add(365 * 24 * time.Hour)
	mu.Lock()
	consents[c.CreatorID] = append(consents[c.CreatorID], c)
	mu.Unlock()
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(c)
}

func dsarHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	var d DSAR
	if err := json.NewDecoder(r.Body).Decode(&d); err != nil {
		http.Error(w, "bad json", http.StatusBadRequest)
		return
	}
	d.Submitted = time.Now()
	d.DueBy = d.Submitted.Add(30 * 24 * time.Hour) // GDPR Art. 12
	mu.Lock()
	dsars[d.CreatorID] = append(dsars[d.CreatorID], d)
	mu.Unlock()
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(d)
}

func dsarStatusHandler(w http.ResponseWriter, r *http.Request) {
	creator := r.URL.Path[len("/v1/dsar/"):]
	mu.RLock()
	defer mu.RUnlock()
	ds, ok := dsars[creator]
	if !ok {
		http.NotFound(w, r)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(ds)
}

func erasureHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	var req struct {
		CreatorID string `json:"creator_id"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "bad json", http.StatusBadRequest)
		return
	}
	mu.Lock()
	delete(consents, req.CreatorID)
	delete(dsars, req.CreatorID)
	mu.Unlock()
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprintf(w, `{"erased":true,"creator_id":%q}`, req.CreatorID)
}

var _ = os.Getenv
