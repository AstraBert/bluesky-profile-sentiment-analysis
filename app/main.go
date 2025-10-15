package main

import (
	"log"
	"sentiment-analysis/handlers"
	"sentiment-analysis/templates"

	"github.com/gofiber/fiber/v2"
)

func main() {
	// Create a new Fiber app
	app := Setup()

	// Start the Fiber server on port 8000
	if err := app.Listen(":8000"); err != nil {
		log.Fatalf("Error starting server: %v", err)
	}
}

func Setup() *fiber.App {
	// Create a new Fiber app
	app := fiber.New()

	app.Post("/analysis", handlers.AnalyzeSentiment)
	app.Get("/", func(c *fiber.Ctx) error {
		c.Set("Content-Type", "text/html")
		return templates.Home().Render(c.Context(), c.Response().BodyWriter())
	})

	return app
}
