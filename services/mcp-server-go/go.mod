module github.com/quantumworld-dpdns-io/mcp-server-go

go 1.22

require (
	github.com/mark3labs/mcp-go v0.10.0
	github.com/rs/zerolog v1.33.0
	github.com/spf13/viper v1.19.0
	github.com/prometheus/client_golang v1.20.5
	go.opentelemetry.io/otel v1.32.0
	go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc v1.32.0
	github.com/redis/go-redis/v9 v9.7.0
	github.com/golang-jwt/jwt/v5 v5.2.1
)
