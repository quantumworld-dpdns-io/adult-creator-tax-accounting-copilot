// Package kyc tests
package kyc

import (
	"context"
	"testing"
	"time"
)

func TestPersonaApproveAdult(t *testing.T) {
	id := Identity{
		CreatorID:   "alice",
		FirstName:   "Alice",
		LastName:    "X",
		DateOfBirth: time.Date(1990, 1, 1, 0, 0, 0, 0, time.UTC),
		Country:     "US",
	}
	res, err := PersonaProvider{}.Screen(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	if res.Decision != DecisionApprove {
		t.Fatalf("want approve, got %s", res.Decision)
	}
	if !res.LivenessOK {
		t.Fatal("liveness should pass")
	}
	if res.AuditHash == "" {
		t.Fatal("audit hash required")
	}
}

func TestPersonaRejectMinor(t *testing.T) {
	id := Identity{
		CreatorID:   "bob",
		DateOfBirth: time.Date(2010, 1, 1, 0, 0, 0, 0, time.UTC),
	}
	res, err := PersonaProvider{}.Screen(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	if res.Decision != DecisionReject {
		t.Fatalf("want reject, got %s", res.Decision)
	}
}

func TestPersonaRequiresCreatorID(t *testing.T) {
	id := Identity{}
	_, err := PersonaProvider{}.Screen(context.Background(), id)
	if err == nil {
		t.Fatal("expected error for empty creator_id")
	}
}
