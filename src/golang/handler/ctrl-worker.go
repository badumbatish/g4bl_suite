package handler

import (
	"net/http"
	"worker/errorutil"

	"github.com/julienschmidt/httprouter"
)

type WorkerAPIHandler struct {
	*httprouter.Router
}

func NewWorkerAPIHandler() *WorkerAPIHandler {
	h := &WorkerAPIHandler{
		Router: httprouter.New(),
	}
	h.Router.GET("/api/start-worker", h.startWorker)

	return h
}

func (h *WorkerAPIHandler) startWorker(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
	_ = errorutil.WriteError(w, func() error {
		defer func() {
			r.Body.Close()
		}()

		return nil
	}())
}
