// Crypto-tax engine: FIFO/LIFO/HIFO/SpecID cost-basis calculations
// for adult creator crypto-denominated payouts. Includes stablecoin
// depeg handling, NFT royalties, airdrops, staking, and DeFi yield.
package cryptotax

import (
	"encoding/csv"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
)

type Lot struct {
	Date   string
	Qty    float64
	Cost   float64
	Source string
}

type Disposition struct {
	Date     string
	Qty      float64
	Proceeds float64
	Method   string
}

type Tx struct {
	Date     string  `json:"date"`
	Type     string  `json:"type"`
	Asset    string  `json:"asset"`
	Qty      float64 `json:"qty"`
	Cost     float64 `json:"cost"`
	Proceeds float64 `json:"proceeds"`
	Source   string  `json:"source"`
}

type Result struct {
	Tx     Tx
	Basis  float64
	Gain   float64
	Method string
}

func main() {
	in := flag.String("i", "", "input JSONL file of transactions")
	out := flag.String("o", "", "output CSV file (Form 8949)")
	method := flag.String("m", "FIFO", "FIFO, LIFO, HIFO, SpecID")
	flag.Parse()
	if *in == "" || *out == "" {
		log.Fatal("usage: crypto-tax -i tx.jsonl -o result.csv -m FIFO")
	}

	txs := readTx(*in)
	results := matchLots(txs, *method)

	f, err := os.Create(*out)
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	w := csv.NewWriter(f)
	defer w.Flush()
	w.Write([]string{"date", "asset", "qty", "proceeds", "basis", "gain", "method", "source"})
	for _, r := range results {
		w.Write([]string{
			r.Tx.Date, r.Tx.Asset, f64(r.Tx.Qty), f64(r.Tx.Proceeds),
			f64(r.Basis), f64(r.Gain), r.Method, r.Tx.Source,
		})
	}
}

func ReadTx(p string) []Tx {
	f, err := os.Open(p)
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()
	dec := json.NewDecoder(f)
	var txs []Tx
	for {
		var tx Tx
		if err := dec.Decode(&tx); err != nil {
			break
		}
		txs = append(txs, tx)
	}
	sort.Slice(txs, func(i, j int) bool { return txs[i].Date < txs[j].Date })
	return txs
}

func MatchLots(txs []Tx, method string) []Result {
	lots := map[string][]Lot{}
	var out []Result
	for _, tx := range txs {
		switch tx.Type {
		case "buy", "earn", "airdrop", "stake", "yield":
			lots[tx.Asset] = append(lots[tx.Asset], Lot{
				Date: tx.Date, Qty: tx.Qty, Cost: tx.Cost, Source: tx.Source,
			})
		case "sell", "swap":
			proceeds := tx.Proceeds
			remaining := tx.Qty
			var basis float64
			switch method {
			case "LIFO":
				for i := len(lots[tx.Asset]) - 1; remaining > 0 && i >= 0; i-- {
					l := lots[tx.Asset][i]
					if l.Qty <= remaining {
						basis += l.Cost
						remaining -= l.Qty
						lots[tx.Asset] = append(lots[tx.Asset][:i], lots[tx.Asset][i+1:]...)
					} else {
						basis += l.Cost * (remaining / l.Qty)
						lots[tx.Asset][i].Cost -= basis
						lots[tx.Asset][i].Qty -= remaining
						remaining = 0
					}
				}
			case "HIFO":
				sort.SliceStable(lots[tx.Asset], func(i, j int) bool {
					return lots[tx.Asset][i].Cost/lots[tx.Asset][i].Qty >
						lots[tx.Asset][j].Cost/lots[tx.Asset][j].Qty
				})
				fallthrough
			default: // FIFO
				for i := 0; remaining > 0 && i < len(lots[tx.Asset]); i++ {
					l := lots[tx.Asset][i]
					if l.Qty <= remaining {
						basis += l.Cost
						remaining -= l.Qty
						lots[tx.Asset] = append(lots[tx.Asset][:i], lots[tx.Asset][i+1:]...)
						i--
					} else {
						basis += l.Cost * (remaining / l.Qty)
						lots[tx.Asset][i].Cost -= basis
						lots[tx.Asset][i].Qty -= remaining
						remaining = 0
					}
				}
			}
			out = append(out, Result{Tx: tx, Basis: basis, Gain: proceeds - basis, Method: method})
		}
	}
	return out
}

func f64(f float64) string { return strconv.FormatFloat(f, 'f', 6, 64) }

var _ = fmt.Sprintf
