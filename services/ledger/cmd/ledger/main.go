// Package ledger implements the double-entry, append-only, hash-chained
// ledger for the Adult Creator Tax & Accounting Copilot.
package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"sync"

	pb "github.com/quantumworld-dpdns-io/ledger/internal/proto"
	"google.golang.org/grpc"
)

type server struct {
	pb.UnimplementedLedgerServer
	mu      sync.RWMutex
	entries map[string]*pb.Entry // key = id
	chain   []string              // hash chain
}

func (s *server) Append(ctx context.Context, req *pb.AppendRequest) (*pb.AppendResponse, error) {
	if req.Entry == nil {
		return &pb.AppendResponse{Ok: false, Error: "nil entry"}, nil
	}
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.entries[req.Entry.Id]; ok {
		return &pb.AppendResponse{Ok: false, Error: "duplicate id"}, nil
	}
	// In production: verify Dilithium signature, verify hash chain.
	s.entries[req.Entry.Id] = req.Entry
	s.chain = append(s.chain, req.Entry.Hash)
	return &pb.AppendResponse{Ok: true, Hash: req.Entry.Hash}, nil
}

func (s *server) Balance(ctx context.Context, req *pb.BalanceRequest) (*pb.BalanceResponse, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	var gross, fees, net float64
	for _, e := range s.entries {
		if e.CreatorId != req.CreatorId || e.Currency != req.Currency {
			continue
		}
		if e.TimestampMs > req.AsOfMs {
			continue
		}
		gross += parse(e.Gross)
		fees += parse(e.Fees)
		net += parse(e.Net)
	}
	return &pb.BalanceResponse{
		Gross: fmt.Sprintf("%.2f", gross),
		Fees:  fmt.Sprintf("%.2f", fees),
		Net:   fmt.Sprintf("%.2f", net),
	}, nil
}

func (s *server) History(ctx context.Context, req *pb.HistoryRequest) (*pb.HistoryResponse, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	var out []*pb.Entry
	for _, e := range s.entries {
		if e.CreatorId != req.CreatorId {
			continue
		}
		if e.TimestampMs < req.StartMs || e.TimestampMs > req.EndMs {
			continue
		}
		out = append(out, e)
	}
	return &pb.HistoryResponse{Entries: out}, nil
}

func (s *server) Reconcile(ctx context.Context, req *pb.ReconcileRequest) (*pb.ReconcileResponse, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	var gross, fees, net float64
	for _, e := range s.entries {
		if e.CreatorId != req.CreatorId || e.TimestampMs > req.PeriodEndMs {
			continue
		}
		gross += parse(e.Gross)
		fees += parse(e.Fees)
		net += parse(e.Net)
	}
	return &pb.ReconcileResponse{Ok: true, Delta: fmt.Sprintf("%.2f", gross-fees-net)}, nil
}

func parse(s string) float64 {
	var f float64
	fmt.Sscanf(s, "%f", &f)
	return f
}

func main() {
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatal(err)
	}
	s := grpc.NewServer()
	pb.RegisterLedgerServer(s, &server{entries: map[string]*pb.Entry{}})
	log.Printf("ledger service listening on :50051")
	if err := s.Serve(lis); err != nil {
		log.Fatal(err)
	}
}
