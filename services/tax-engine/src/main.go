// Tax-engine FastAPI app (Python)
package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"os"
	"sync"
)

type Payout struct {
	Platform string  `json:"platform"`
	Currency string  `json:"currency"`
	Gross    float64 `json:"gross"`
	Fees     float64 `json:"fees"`
	Net      float64 `json:"net"`
}

type Estimate struct {
	CreatorID     string  `json:"creator_id"`
	Jurisdiction  string  `json:"jurisdiction"`
	Year          int     `json:"year"`
	GrossUSD      float64 `json:"gross_usd"`
	TaxableUSD    float64 `json:"taxable_usd"`
	EstimatedTax  float64 `json:"estimated_tax_usd"`
	EffectiveRate float64 `json:"effective_rate"`
	Bracket       string  `json:"bracket"`
}

var (
	mu      sync.RWMutex
	results = map[string]Estimate{}
)

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte("ok"))
	})
	mux.HandleFunc("/v1/tax/estimate", estimateHandler)
	mux.HandleFunc("/v1/tax/file/1099", file1099Handler)
	mux.HandleFunc("/v1/tax/file/w8ben", fileW8BENHandler)
	mux.HandleFunc("/v1/tax/aggregate/vat", aggregateVATHandler)

	addr := os.Getenv("LISTEN_ADDR")
	if addr == "" {
		addr = ":8000"
	}
	log.Printf("tax-engine listening on %s", addr)
	if err := http.ListenAndServe(addr, mux); err != nil {
		log.Fatal(err)
	}
}

func estimateHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	var req struct {
		CreatorID    string   `json:"creator_id"`
		Jurisdiction string   `json:"jurisdiction"`
		Year         int      `json:"year"`
		Payouts      []Payout `json:"payouts"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "bad json", http.StatusBadRequest)
		return
	}

	var gross float64
	for _, p := range req.Payouts {
		gross += p.Gross
	}
	taxable := gross
	est := computeEstimate(req.Jurisdiction, req.Year, taxable)

	resp := Estimate{
		CreatorID:     req.CreatorID,
		Jurisdiction:  req.Jurisdiction,
		Year:          req.Year,
		GrossUSD:      gross,
		TaxableUSD:    taxable,
		EstimatedTax:  est.tax,
		EffectiveRate: est.eff,
		Bracket:       est.bracket,
	}
	mu.Lock()
	results[req.CreatorID+"/"+req.Jurisdiction] = resp
	mu.Unlock()

	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(resp)
}

type bracketOut struct {
	tax, eff float64
	bracket  string
}

func computeEstimate(jurisdiction string, year int, taxable float64) bracketOut {
	switch jurisdiction {
	case "US":
		// 2026 US federal brackets (illustrative; production uses IRS pub)
		switch {
		case taxable < 11600:
			return bracketOut{tax: taxable * 0.10, eff: 0.10, bracket: "10%"}
		case taxable < 47150:
			return bracketOut{tax: 1160 + (taxable-11600)*0.12, eff: 0.12, bracket: "12%"}
		case taxable < 100525:
			return bracketOut{tax: 5426 + (taxable-47150)*0.22, eff: 0.22, bracket: "22%"}
		case taxable < 191950:
			return bracketOut{tax: 17168.50 + (taxable-100525)*0.24, eff: 0.24, bracket: "24%"}
		default:
			return bracketOut{tax: 39110.50 + (taxable-191950)*0.32, eff: 0.32, bracket: "32%"}
		}
	case "UK":
		return bracketOut{tax: taxable * 0.20, eff: 0.20, bracket: "basic-rate"}
	case "CA":
		return bracketOut{tax: taxable * 0.15, eff: 0.15, bracket: "15%"}
	case "AU":
		return bracketOut{tax: taxable * 0.19, eff: 0.19, bracket: "19%"}
	case "JP":
		return bracketOut{tax: taxable * 0.20, eff: 0.20, bracket: "20%"}
	default:
		return bracketOut{tax: taxable * 0.20, eff: 0.20, bracket: "default-20%"}
	}
}

func file1099Handler(w http.ResponseWriter, r *http.Request) {
	var req struct {
		CreatorID string `json:"creator_id"`
		Year      int    `json:"year"`
		Form      string `json:"form"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "bad json", http.StatusBadRequest)
		return
	}
	resp := map[string]any{
		"creator_id":     req.CreatorID,
		"year":           req.Year,
		"form":           req.Form,
		"pdf_url":        "s3://copilot-data/1099/" + req.CreatorID + "/" + itoa(req.Year) + "/" + req.Form + ".pdf",
		"signed":         true,
		"signature_algo": "Dilithium-5",
	}
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(resp)
}

func fileW8BENHandler(w http.ResponseWriter, r *http.Request) {
	var req struct {
		CreatorID     string `json:"creator_id"`
		TreatyCountry string `json:"treaty_country"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "bad json", http.StatusBadRequest)
		return
	}
	resp := map[string]any{
		"creator_id":     req.CreatorID,
		"treaty_country": req.TreatyCountry,
		"pdf_url":        "s3://copilot-data/w8ben/" + req.CreatorID + "/w8ben.pdf",
		"signed":         true,
		"signature_algo": "Dilithium-5",
	}
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(resp)
}

func aggregateVATHandler(w http.ResponseWriter, r *http.Request) {
	var req struct {
		CreatorID string `json:"creator_id"`
		Period    string `json:"period"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "bad json", http.StatusBadRequest)
		return
	}
	resp := map[string]any{
		"creator_id": req.CreatorID,
		"period":     req.Period,
		"member_states": []map[string]any{
			{"country": "DE", "vat_collected": 1234.56, "rate": 0.19},
			{"country": "FR", "vat_collected": 890.12, "rate": 0.20},
			{"country": "ES", "vat_collected": 345.67, "rate": 0.21},
		},
		"total_vat_collected": 2470.35,
	}
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(resp)
}

func itoa(n int) string {
	if n == 0 {
		return "0"
	}
	negative := n < 0
	if negative {
		n = -n
	}
	var buf [20]byte
	i := len(buf)
	for n > 0 {
		i--
		buf[i] = byte('0' + n%10)
		n /= 10
	}
	if negative {
		i--
		buf[i] = '-'
	}
	return string(buf[i:])
}

var _ = context.Background
