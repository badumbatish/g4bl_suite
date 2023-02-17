package main

import (
	"log"
	"net/http"
	"strings"
	"worker/handler"

	"github.com/spf13/viper"
)

type HandlerList []interface{}

func (hl HandlerList) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()

	if ctx.Err() != nil {
		return
	}

	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
	w.Header().Set("Access-Control-Allow-Headers", "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")

	for _, h := range hl {
		handler, ok := h.(http.Handler)
		if ok {
			handler.ServeHTTP(w, r)
			continue
		}

		panic("Not a handler")
	}

}

func main() {
	viper.SetEnvKeyReplacer(strings.NewReplacer("-", "_"))
	viper.AutomaticEnv()

	viper.SetConfigName("worker")

	viper.AddConfigPath("/app/etc")
	viper.SetConfigType("yaml")

	err := viper.ReadInConfig()
	if err != nil {
		panic(err)
	}

	testVar := viper.GetString("test-config")

	handlerList := HandlerList{}

	workerHandler := handler.NewWorkerAPIHandler()
	handlerList = append(handlerList, workerHandler)

	log.Println(testVar)

	http.ListenAndServe(":80", handlerList)
}
