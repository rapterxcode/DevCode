package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

// Item struct สำหรับเก็บข้อมูลตัวอย่าง
type Item struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}

var items = []Item{
	{ID: 1, Name: "Item 1"},
	{ID: 2, Name: "Item 2"},
}

func pingHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"message": "pong"})
}

// GET /items - ดึงรายการทั้งหมด
func getItemsHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(items)
}

// POST /items - เพิ่มรายการใหม่
func createItemHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	var newItem Item
	if err := json.NewDecoder(r.Body).Decode(&newItem); err != nil {
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(map[string]string{"error": "Invalid request body"})
		return
	}
	newItem.ID = len(items) + 1
	items = append(items, newItem)
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(newItem)
}

// PUT /items/{id} - อัปเดตรายการ
func updateItemHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	id := 0
	_, err := fmt.Sscanf(r.URL.Path, "/items/%d", &id)
	if err != nil || id < 1 {
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(map[string]string{"error": "Invalid ID"})
		return
	}
	var updated Item
	if err := json.NewDecoder(r.Body).Decode(&updated); err != nil {
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(map[string]string{"error": "Invalid request body"})
		return
	}
	for i, item := range items {
		if item.ID == id {
			items[i].Name = updated.Name
			json.NewEncoder(w).Encode(items[i])
			return
		}
	}
	w.WriteHeader(http.StatusNotFound)
	json.NewEncoder(w).Encode(map[string]string{"error": "Item not found"})
}

// DELETE /items/{id} - ลบรายการ
func deleteItemHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	id := 0
	_, err := fmt.Sscanf(r.URL.Path, "/items/%d", &id)
	if err != nil || id < 1 {
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(map[string]string{"error": "Invalid ID"})
		return
	}
	for i, item := range items {
		if item.ID == id {
			items = append(items[:i], items[i+1:]...)
			json.NewEncoder(w).Encode(map[string]string{"message": "Item deleted"})
			return
		}
	}
	w.WriteHeader(http.StatusNotFound)
	json.NewEncoder(w).Encode(map[string]string{"error": "Item not found"})
}

func main() {
	http.HandleFunc("/ping", pingHandler)
	http.HandleFunc("/items", func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case http.MethodGet:
			getItemsHandler(w, r)
		case http.MethodPost:
			createItemHandler(w, r)
		default:
			w.WriteHeader(http.StatusMethodNotAllowed)
		}
	})
	http.HandleFunc("/items/", func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case http.MethodPut:
			updateItemHandler(w, r)
		case http.MethodDelete:
			deleteItemHandler(w, r)
		default:
			w.WriteHeader(http.StatusMethodNotAllowed)
		}
	})
	fmt.Println("Server started at http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
