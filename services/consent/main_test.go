// Package consent tests
package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestConsentHandler(t *testing.T) {
	body := bytes.NewBufferString(`{"creator_id":"alice","purposes":["marketing","analytics"],"granted":true}`)
	req := httptest.NewRequest(http.MethodPost, "/v1/consent", body)
	w := httptest.NewRecorder()
	consentHandler(w, req)
	if w.Code != 200 {
		t.Fatalf("want 200, got %d", w.Code)
	}
	var c Consent
	if err := json.NewDecoder(w.Body).Decode(&c); err != nil {
		t.Fatal(err)
	}
	if c.CreatorID != "alice" {
		t.Fatalf("creator_id mismatch")
	}
}

func TestDSARHandler(t *testing.T) {
	body := bytes.NewBufferString(`{"creator_id":"alice","type":"erasure"}`)
	req := httptest.NewRequest(http.MethodPost, "/v1/dsar", body)
	w := httptest.NewRecorder()
	dsarHandler(w, req)
	if w.Code != 200 {
		t.Fatalf("want 200, got %d", w.Code)
	}
}

func TestErasureHandler(t *testing.T) {
	body := bytes.NewBufferString(`{"creator_id":"alice"}`)
	req := httptest.NewRequest(http.MethodPost, "/v1/gdpr/erasure", body)
	w := httptest.NewRecorder()
	erasureHandler(w, req)
	if w.Code != 200 {
		t.Fatalf("want 200, got %d", w.Code)
	}
	if !bytes.Contains(w.Body.Bytes(), []byte(`"erased":true`)) {
		t.Fatal("missing erased marker")
	}
}
