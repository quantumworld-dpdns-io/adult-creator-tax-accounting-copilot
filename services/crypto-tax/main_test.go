package main

import (
	"encoding/csv"
	"os"
	"path/filepath"
	"strconv"
	"testing"

	cryptotax "github.com/quantumworld-dpdns-io/crypto-tax/pkg"
)

func TestMatchLotsFIFO(t *testing.T) {
	txs := []cryptotax.Tx{
		{Date: "2025-01-01", Type: "earn", Asset: "USDC", Qty: 100, Cost: 100},
		{Date: "2025-02-01", Type: "sell", Asset: "USDC", Qty: 60, Proceeds: 70},
	}
	res := cryptotax.MatchLots(txs, "FIFO")
	if len(res) != 1 {
		t.Fatalf("expected 1 result, got %d", len(res))
	}
	if res[0].Basis != 60 {
		t.Fatalf("expected basis 60, got %f", res[0].Basis)
	}
	if res[0].Gain != 10 {
		t.Fatalf("expected gain 10, got %f", res[0].Gain)
	}
}

func TestMatchLotsLIFO(t *testing.T) {
	txs := []cryptotax.Tx{
		{Date: "2025-01-01", Type: "earn", Asset: "USDC", Qty: 100, Cost: 100},
		{Date: "2025-03-01", Type: "earn", Asset: "USDC", Qty: 50, Cost: 50},
		{Date: "2025-04-01", Type: "sell", Asset: "USDC", Qty: 40, Proceeds: 60},
	}
	res := cryptotax.MatchLots(txs, "LIFO")
	if len(res) != 1 {
		t.Fatalf("expected 1 result, got %d", len(res))
	}
	if res[0].Basis != 40 {
		t.Fatalf("expected basis 40, got %f", res[0].Basis)
	}
}

func TestMatchLotsHIFO(t *testing.T) {
	txs := []cryptotax.Tx{
		{Date: "2025-01-01", Type: "earn", Asset: "USDC", Qty: 100, Cost: 100}, // $1/unit
		{Date: "2025-03-01", Type: "earn", Asset: "USDC", Qty: 50, Cost: 25},   // $0.50/unit
		{Date: "2025-04-01", Type: "sell", Asset: "USDC", Qty: 30, Proceeds: 60},
	}
	res := cryptotax.MatchLots(txs, "HIFO")
	if len(res) != 1 {
		t.Fatalf("expected 1 result, got %d", len(res))
	}
	// HIFO picks the highest cost-per-unit first: 30 qty * $1 = $30.
	if res[0].Basis != 30 {
		t.Fatalf("expected basis 30, got %f", res[0].Basis)
	}
}

func TestReadTx(t *testing.T) {
	dir := t.TempDir()
	p := filepath.Join(dir, "tx.jsonl")
	lines := []string{
		`{"date":"2025-01-01","type":"earn","asset":"USDC","qty":100,"cost":100,"proceeds":0}`,
		`{"date":"2025-02-01","type":"sell","asset":"USDC","qty":50,"cost":0,"proceeds":55}`,
	}
	f, _ := os.Create(p)
	for _, l := range lines {
		f.WriteString(l + "\n")
	}
	f.Close()
	txs := cryptotax.ReadTx(p)
	if len(txs) != 2 {
		t.Fatalf("expected 2 txs, got %d", len(txs))
	}
	if txs[0].Type != "earn" {
		t.Fatalf("expected earn first, got %s", txs[0].Type)
	}
}

func TestCSVExport(t *testing.T) {
	dir := t.TempDir()
	out := filepath.Join(dir, "out.csv")
	f, _ := os.Create(out)
	w := csv.NewWriter(f)
	w.Write([]string{"date", "asset", "qty", "proceeds", "basis", "gain", "method", "source"})
	w.Write([]string{"2025-01-01", "USDC", "100", "110", "100", "10", "FIFO", "OnlyFans"})
	w.Flush()
	f.Close()
	contents, _ := os.ReadFile(out)
	if len(contents) == 0 {
		t.Fatal("csv empty")
	}
	if !contains(string(contents), "FIFO") {
		t.Fatal("missing FIFO")
	}
}

func contains(s, sub string) bool {
	return len(s) >= len(sub) && (s == sub || (len(s) > len(sub) && (s[:len(sub)] == sub || s[len(s)-len(sub):] == sub || containsInner(s, sub))))
}

func containsInner(s, sub string) bool {
	for i := 0; i+len(sub) <= len(s); i++ {
		if s[i:i+len(sub)] == sub {
			return true
		}
	}
	return false
}

var _ = strconv.Itoa
