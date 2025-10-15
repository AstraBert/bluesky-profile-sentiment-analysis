package handlers

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"sentiment-analysis/commons"
	"sentiment-analysis/templates"

	"github.com/gofiber/fiber/v2"
)

func AnalyzeSentiment(c *fiber.Ctx) error {
	inputData := c.FormValue("userHandle")
	if inputData == "" {
		return templates.ErrorBanner(errors.New("you have to provide a user handle")).Render(c.Context(), c.Response().BodyWriter())
	}
	inputEvent := commons.InputEvent{UserHandle: inputData}
	requestBody := commons.RequestBody{StartEvent: inputEvent, Context: map[string]any{}, HandlerId: ""}
	apiKey := os.Getenv("LLAMA_CLOUD_API_KEY")
	apiEndpoint := os.Getenv("LLAMA_CLOUD_API_ENDPOINT")
	jsonData, err := json.Marshal(requestBody)

	c.Set("Content-Type", "text/html")
	if err != nil {
		return templates.ErrorBanner(err).Render(c.Context(), c.Response().BodyWriter())
	}

	// Create the HTTP request
	req, err := http.NewRequest("POST", apiEndpoint, bytes.NewBuffer(jsonData))
	if err != nil {
		return templates.ErrorBanner(err).Render(c.Context(), c.Response().BodyWriter())
	}

	// Set headers
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+apiKey)

	// Send the request
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return templates.ErrorBanner(err).Render(c.Context(), c.Response().BodyWriter())
	}
	defer resp.Body.Close()

	// Read the response
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return templates.ErrorBanner(err).Render(c.Context(), c.Response().BodyWriter())
	}

	// Check status code
	if resp.StatusCode != http.StatusOK {
		return templates.ErrorBanner(fmt.Errorf("response has status %d: %s", resp.StatusCode, string(body))).Render(c.Context(), c.Response().BodyWriter())
	}

	var response commons.ResponseBody

	err = json.Unmarshal(body, &response)

	if err != nil {
		return templates.ErrorBanner(err).Render(c.Context(), c.Response().BodyWriter())
	}

	if response.Error != nil {
		return templates.ErrorBanner(errors.New(*response.Error)).Render(c.Context(), c.Response().BodyWriter())
	}

	return templates.Analysis(inputData, response.Result.AllSentiments, *response.Result.PrevailingSentiment, *response.Result.AverageConfidenceScore).Render(c.Context(), c.Response().BodyWriter())
}
