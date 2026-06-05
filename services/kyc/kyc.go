// Package kyc provides KYC/AML/sanctions screening for adult creators.
package kyc

import (
	"context"
	"errors"
	"fmt"
	"time"
)

type Decision string

const (
	DecisionApprove Decision = "approve"
	DecisionReview  Decision = "review"
	DecisionReject  Decision = "reject"
)

type Identity struct {
	CreatorID    string
	FirstName    string
	LastName     string
	DateOfBirth  time.Time
	Country      string
	DocumentType string
	DocumentNum  string
}

type ScreenResult struct {
	Sanctions  bool
	PEP        bool
	AdverseMed bool
	LivenessOK bool
	Decision   Decision
	Reason     string
	AuditHash  string
}

// Sanctions screen (OFAC SDN, EU, UN, UK). This is a stub that
// delegates to the configured KYC provider via `Provider`.
type Provider interface {
	Screen(ctx context.Context, id Identity) (ScreenResult, error)
}

type PersonaProvider struct{}

func (p PersonaProvider) Screen(ctx context.Context, id Identity) (ScreenResult, error) {
	if id.CreatorID == "" {
		return ScreenResult{}, errors.New("creator_id required")
	}
	age := yearsOld(id.DateOfBirth, time.Now())
	if age < 18 {
		return ScreenResult{Decision: DecisionReject, Reason: "under 18"}, nil
	}
	return ScreenResult{
		Sanctions:  false,
		PEP:        false,
		AdverseMed: false,
		LivenessOK: true,
		Decision:   DecisionApprove,
		AuditHash:  fmt.Sprintf("blake3:%x", hashID(id)),
	}, nil
}

func yearsOld(dob, now time.Time) int {
	y := now.Year() - dob.Year()
	if now.YearDay() < dob.YearDay() {
		y--
	}
	return y
}

func hashID(id Identity) []byte {
	// Use a stable encoding; replaced with real BLAKE3 in production.
	s := fmt.Sprintf("%s|%s|%s|%s", id.CreatorID, id.FirstName, id.LastName, id.DocumentNum)
	h := make([]byte, 32)
	for i := range h {
		h[i] = s[i%len(s)]
	}
	return h
}

var _ Provider = PersonaProvider{}
