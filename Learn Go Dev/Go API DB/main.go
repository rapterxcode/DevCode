package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"

	_ "github.com/go-sql-driver/mysql"
)

var db *sql.DB

func main() {
	var err error
	// TODO: เปลี่ยน user:password@tcp(localhost:3306)/dbname ให้ตรงกับ MySQL ของคุณ
	dsn := "user:password@tcp(localhost:3306)/testdb"
	db, err = sql.Open("mysql", dsn)
	if err != nil {
		log.Fatal("Cannot connect to DB:", err)
	}
	if err = db.Ping(); err != nil {
		log.Fatal("Cannot ping DB:", err)
	}
	fmt.Println("Connected to MySQL!")

	http.HandleFunc("/ping", pingHandler)
	http.HandleFunc("/items", itemsHandler)
	http.HandleFunc("/items/", itemHandler)
	fmt.Println("Server started at http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func pingHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprintln(w, `{"message": "pong"}`)
}

func itemsHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		// TODO: getItemsFromDB(w, r)
	case http.MethodPost:
		// TODO: createItemInDB(w, r)
	default:
		w.WriteHeader(http.StatusMethodNotAllowed)
	}
}

func itemHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodPut:
		// TODO: updateItemInDB(w, r)
	case http.MethodDelete:
		// TODO: deleteItemInDB(w, r)
	default:
		w.WriteHeader(http.StatusMethodNotAllowed)
	}
}
