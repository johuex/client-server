package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

type Message struct {
	Username string
	Message  string
	Time     string
}

type MessageRequest struct {
	Username string
	Password string
	Message  string
	Time     string
}

type Status struct {
	Status         bool
	Time           string
	Messages_count int
	Users_count    int
}

var messages []Message

var users = make(map[string]string)

func status(w http.ResponseWriter, r *http.Request) {
	s := Status{Status: true, Time: time.Now().String(), Messages_count: len(messages), Users_count: len(users)}
	sendJSONRepsonse(w, http.StatusOK, s)
}

func send(w http.ResponseWriter, r *http.Request) {
	var mr MessageRequest
	reqBody, _ := ioutil.ReadAll(r.Body)
	json.Unmarshal(reqBody, &mr)

	passwd := mr.Password
	real_passwd, ok := users["username"] // TODO
	payload := make(map[string]bool)
	if ok {
		if passwd != real_passwd {
			payload["ok"] = false
			sendJSONRepsonse(w, http.StatusOK, payload)
		}
	} else {
		users["username"] = passwd
	}

	_ = append(messages, Message{"username", "message", time.Now().String()})
	payload["ok"] = false
	sendJSONRepsonse(w, http.StatusOK, payload)
}

func history(w http.ResponseWriter, r *http.Request) {
	keys, _ := r.URL.Query()["after"]
	after := keys[0]
	//after, _ := strconv.ParseInt(keys[0], 10, 64)
	mes := []Message{}
	for i := range messages {
		if messages[i].Time < after {
			_ = append(mes, messages[i])
		}
	}
	payload := make(map[string][]Message)
	payload["messages"] = mes
	sendJSONRepsonse(w, http.StatusOK, payload)
}

func sendJSONRepsonse(w http.ResponseWriter, status int, payload interface{}) {
	response, _ := json.Marshal(payload)
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	w.Write(response)
}

func handleRequests() {
	myRouter := mux.NewRouter().StrictSlash(true)
	myRouter.HandleFunc("/status", status)
	myRouter.HandleFunc("/send", send).Methods("POST")
	myRouter.HandleFunc("/history", history)
	http.Handle("/", myRouter)
	log.Fatal(http.ListenAndServe(":10000", myRouter))
}

func main() {
	_ = append(messages, Message{Username: "Messenger", Message: "Please, login to send messages!", Time: time.Now().String()})
	handleRequests()
}
