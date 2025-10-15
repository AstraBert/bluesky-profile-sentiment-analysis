package commons

type InputEvent struct {
	UserHandle string `json:"user_handle"`
}

type RequestBody struct {
	StartEvent InputEvent     `json:"start_event"`
	Context    map[string]any `json:"contenxt"`
	HandlerId  string         `json:"handler_id"`
}

// {'all_sentiments': ['NEUTRAL', 'none', 'POSITIVE', 'joy', 'surprise'], 'prevailing_sentiment': 'POSITIVE', 'average_confidence_score': 1.0, 'error': None}

type ResponseResult struct {
	AllSentiments          []string `json:"all_sentiments"`
	PrevailingSentiment    *string  `json:"prevailing_sentiment"`
	AverageConfidenceScore *float64 `json:"average_confidence_score"`
	Error                  *string  `json:"error"`
}

type ResponseBody struct {
	HandlerId    string          `json:"handler_id"`
	WorkflowName string          `json:"workflow_name"`
	RunId        string          `json:"run_id"`
	Status       string          `json:"status"`
	StartedAt    *string         `json:"started_at"`
	UpdatedAt    *string         `json:"updated_at"`
	CompletedAt  *string         `json:"completed_at"`
	Error        *string         `json:"error"`
	Result       *ResponseResult `json:"result"`
}
