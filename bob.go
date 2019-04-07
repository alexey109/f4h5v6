package main

import (
	"encoding/json"
	"fmt" // пакет для форматированного ввода вывода
	"io/ioutil"
	"log"      // пакет для логирования
	"math"
	"math/rand"
	"net/http" // пакет для поддержки HTTP протокола
)

type postData struct {
	P1 int
	P2 int
	P3 float64
}

var b = rand.Intn(100)
var B float64
var p float64
var step = 1

func ServerHandler(w http.ResponseWriter, r *http.Request) {
	body, _ := ioutil.ReadAll(r.Body)
	fmt.Println("request Body:", string(body))

	var resp postData
	_ = json.Unmarshal(body, &resp)

	switch step {
	// получение P и генерация публичного ключа
	case 1:
		fmt.Println("b =", b)
		step += 1
		p = float64(resp.P1)
		pw := math.Pow(float64(resp.P2), float64(b))
		B = math.Mod(pw, p)

		requestData := &postData{
			P1: 0,
			P2: 0,
			P3: B,
		}
		jsonData, _ := json.Marshal(requestData)
		strData := string(jsonData)
		fmt.Println("Возвращаем B:", requestData.P3)

		_, _ = fmt.Fprintf(w, strData) // отправляем данные на клиентскую сторону
	case 2:
		step += 1
		pw := math.Pow(resp.P3, float64(b))
		K := math.Mod(pw, p)

		fmt.Println("K = ", K)

		_, _ = fmt.Fprintf(w, "Success") // отправляем данные на клиентскую сторону
	default:
		_, _ = fmt.Fprintf(w, "Hi") // отправляем данные на клиентскую сторону
	}
}

func main() {
	http.HandleFunc("/", ServerHandler)      // установим метод обработки запросов
	err := http.ListenAndServe(":9000", nil) // задаем слушать порт
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}