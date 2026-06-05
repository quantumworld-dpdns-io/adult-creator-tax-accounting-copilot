package main

import (
	"bytes"
	"encoding/json"
	"os"
	"path/filepath"
	"testing"
)

func writeTxFile(t *testing.T, lines []string) string {
	t.Helper()
	dir := t.TempDir()
	p := filepath.Join(dir, "tx.jsonl")
	if err := os.WriteFile(p, []byte(""), 0o644); err != nil {
		t.Fatal(err)
	}
	f, err := os.OpenFile(p, os.O_APPEND|os.O_WRONLY, 0o644)
	if err != nil {
		t.Fatal(err)
	}
	defer f.Close()
	for _, l := range lines {
		if _, err := f.WriteString(l + "\n"); err != nil {
			t.Fatal(err)
		}
	}
	return p
}

func TestMatchLotsFIFO(t *testing.T) {
	txs := []Tx{
		{Date: "2025-01-01", Type: "earn", Asset: "USDC", Qty: 100, Cost: 100},
		{Date: "2025-02-01", Type: "sell", Asset: "USDC", Qty: 60, Proceeds: 70},
	}
	res := matchLots(txs, "FIFO")
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
	txs := []Tx{
		{Date: "2025-01-01", Type: "earn", Asset: "USDC", Qty: 100, Cost: 100},
		{Date: "2025-03-01", Type: "earn", Asset: "USDC", Qty: 50, Cost: 50},
		{Date: "2025-04-01", Type: "sell", Asset: "USDC", Qty: 40, Proceeds: 60},
	}
	res := matchLots(txs, "LIFO")
	if len(res) != 1 {
		t.Fatalf("expected 1 result, got %d", len(res))
	}
	if res[0].Basis != 40 {
		t.Fatalf("expected basis 40, got %f", res[0].Basis)
	}
}

func TestReadTx(t *testing.T) {
	lines := []string{
		`{"date":"2025-01-01","type":"earn","asset":"USDC","qty":100,"cost":100,"proceeds":0}`,
		`{"date":"2025-02-01","type":"sell","asset":"USDC","qty":50,"cost":0,"proceeds":55}`,
	}
	p := writeTxFile(t, lines)
	txs := readTx(p)
	if len(txs) != 2 {
		t.Fatalf("expected 2 txs, got %d", len(txs))
	}
	if txs[0].Type != "earn" {
		t.Fatalf("expected earn first")
	}
}

func TestMainRuns(t *testing.T) {
	lines := []string{
		`{"date":"2025-01-01","type":"earn","asset":"USDC","qty":100,"cost":100,"proceeds":0}`,
	}
	p := writeTxFile(t, lines)
	dir := t.TempDir()
	out := filepath.Join(dir, "out.csv")
	oldOut, _ := os.Create(out)
	defer oldOut.Close()
	if err := os.WriteFile(out, []byte{}, 0o644); err != nil {
		t.Fatal(err)
	}
	txs := readTx(p)
	results := matchLots(txs, "FIFO")
	if len(results) == 0 {
		t.Fatal("expected results")
	}
}

func TestParse(t *testing.T) {
	if parse("123.45") != 123.45 {
		t.Fatal("parse failed")
	}
	if parse("0") != 0 {
		t.Fatal("parse 0 failed")
	}
}

var _ = bytes.NewBuffer
var _ = json.Marshal
