package errorutil

import (
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"
	"runtime"
)

type ErrorCoder interface {
	ErrorCode() int
}

type ErrorShower interface {
	ErrorShow() string
}

type ErrorLocer interface {
	ErrorLoc() string
}

type WebError struct {
	ErrText string `json:"error"`
}

type webErrDetail struct {
	code int    // HTTP status code
	loc  string // Location of error
	show string // Error message to show to user
	err  error  // Error to log
}

func (e *webErrDetail) Error() string {
	return fmt.Sprintf("WebErrorDetail: code=%d, show=%q, loc=%q, err: %s", e.code, e.show, e.loc, e.err.Error())
}

func (e *webErrDetail) ErrorLoc() string {
	return e.loc
}

func (e *webErrDetail) ErrorShow() string {
	return e.show
}

func (e *webErrDetail) ErrorCode() int {
	if e.code == 0 {
		return http.StatusInternalServerError
	}

	return e.code
}

func WriteError(w http.ResponseWriter, err error) error {
	if err == nil {
		return nil
	}

	log.Printf("Error: %v", err.Error())

	w.Header().Set("Content-Type", "application/json")

	var statusCode int
	var coder ErrorCoder
	if errors.As(err, &coder) {
		statusCode = coder.ErrorCode()
	} else {
		statusCode = http.StatusInternalServerError
	}

	var showStr string
	var showErr ErrorShower
	if errors.As(err, &showErr) {
		showStr = showErr.ErrorShow()
	} else {
		showStr = "internal error"
	}

	webError := WebError{
		ErrText: showStr,
	}

	return WriteJSON(w, webError, statusCode)
}

func WriteJSON(w http.ResponseWriter, v interface{}, status int) error {
	w.Header().Set("Content-Type", "application/json")

	w.WriteHeader(status)

	jsonBytes, err := json.Marshal(v)
	if err != nil {
		return err
	}

	_, err = w.Write(jsonBytes)

	return err
}

func ErrorCodeShowf(code int, cause error, fmtstr string, args ...interface{}) error {
	showStr := fmt.Sprintf(fmtstr, args...)

	if cause == nil {
		cause = errors.New(showStr)
	}

	_, file, line, _ := runtime.Caller(1)

	ret := webErrDetail{
		code: code,
		loc:  fmt.Sprintf("%s:%d", file, line),
		show: showStr,
		err:  cause,
	}

	return &ret
}
