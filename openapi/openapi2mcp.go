// Generated OpenAPI → MCP tool generator.
//
// Reads an OpenAPI 3.1 spec and emits a list of MCP tool definitions in
// JSON or YAML. Usage:
//   go run ./cmd/openapi2mcp -i spec.yaml -o tools.json
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"

	"sigs.k8s.io/yaml"
)

type OpenAPI struct {
	Paths map[string]map[string]Operation `json:"paths"`
}

type Operation struct {
	OperationID string                 `json:"operationId"`
	Summary     string                 `json:"summary"`
	Description string                 `json:"description"`
	Parameters  []Parameter            `json:"parameters"`
	RequestBody map[string]interface{} `json:"requestBody"`
}

type Parameter struct {
	Name        string                 `json:"name"`
	In          string                 `json:"in"`
	Required    bool                   `json:"required"`
	Schema      map[string]interface{} `json:"schema"`
	Description string                 `json:"description"`
}

type Tool struct {
	Name        string                 `json:"name"`
	Description string                 `json:"description"`
	InputSchema map[string]interface{} `json:"inputSchema"`
}

func main() {
	in := flag.String("i", "", "input OpenAPI YAML/JSON file")
	out := flag.String("o", "", "output MCP tools JSON file")
	flag.Parse()
	if *in == "" || *out == "" {
		fmt.Fprintln(os.Stderr, "usage: openapi2mcp -i spec.yaml -o tools.json")
		os.Exit(2)
	}
	spec, err := os.ReadFile(*in)
	must(err)
	var api OpenAPI
	if isJSON(spec) {
		must(json.Unmarshal(spec, &api))
	} else {
		must(yaml.Unmarshal(spec, &api))
	}

	var tools []Tool
	for path, methods := range api.Paths {
		for method, op := range methods {
			t := Tool{
				Name:        op.OperationID,
				Description: first(op.Summary, op.Description, fmt.Sprintf("%s %s", method, path)),
				InputSchema: buildSchema(op),
			}
			tools = append(tools, t)
		}
	}
	enc, err := json.MarshalIndent(tools, "", "  ")
	must(err)
	must(os.WriteFile(*out, enc, 0o644))
}

func buildSchema(op Operation) map[string]interface{} {
	props := map[string]interface{}{}
	required := []string{}
	for _, p := range op.Parameters {
		props[p.Name] = map[string]interface{}{
			"type":        p.Schema["type"],
			"description": p.Description,
		}
		if p.Required {
			required = append(required, p.Name)
		}
	}
	s := map[string]interface{}{"type": "object", "properties": props}
	if len(required) > 0 {
		s["required"] = required
	}
	return s
}

func first(xs ...string) string {
	for _, x := range xs {
		if x != "" {
			return x
		}
	}
	return ""
}

func isJSON(b []byte) bool {
	for _, c := range b {
		if c == ' ' || c == '\n' || c == '\t' {
			continue
		}
		return c == '{'
	}
	return false
}

func must(err error) {
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
