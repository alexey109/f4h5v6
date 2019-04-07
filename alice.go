package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math"
	"math/rand"
	"net/http"
)

const N = 100

func getPrime() int {
	var x, y, n int
	nsqrt := math.Sqrt(N)

	is_prime := [N]bool{}

	for x = 1; float64(x) <= nsqrt; x++ {
		for y = 1; float64(y) <= nsqrt; y++ {
			n = 4*(x*x) + y*y
			if n <= N && (n%12 == 1 || n%12 == 5) {
				is_prime[n] = !is_prime[n]
			}
			n = 3*(x*x) + y*y
			if n <= N && n%12 == 7 {
				is_prime[n] = !is_prime[n]
			}
			n = 3*(x*x) - y*y
			if x > y && n <= N && n%12 == 11 {
				is_prime[n] = !is_prime[n]
			}
		}
	}

	for n = 5; float64(n) <= nsqrt; n++ {
		if is_prime[n] {
			for y = n * n; y < N; y += n * n {
				is_prime[y] = false
			}
		}
	}

	is_prime[2] = true
	is_prime[3] = true

	primes := make([]int, 0, 1270606)
	for x = 0; x < len(is_prime)-1; x++ {
		if is_prime[x] {
			primes = append(primes, x)
		}
	}

	return primes[len(primes)-1]
}

type postData struct {
	P1 int
	P2 int
	P3 float64
}

func sendRequest(v1 int, v2 int, v3 float64) (postData, error) {
	url := "http://127.0.0.1:9000/"

	requestData := &postData{
		P1: v1,
		P2: v2,
		P3: v3,
	}

	jsonData, _ := json.Marshal(requestData)
	strData := string(jsonData)
	fmt.Println("Отправляем p, g, a:", requestData.P1, requestData.P2, requestData.P3)

	req, err := http.NewRequest("POST", url, bytes.NewReader([]byte(strData)))
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return *requestData, err
	}

	fmt.Println("response Status:", resp.Status)
	body, _ := ioutil.ReadAll(resp.Body)
	fmt.Println("response Body:", string(body))

	var resp2 postData
	_ = json.Unmarshal(body, &resp2)

	err = resp.Body.Close()

	return resp2, err
}

func sendPg() error {
	a := rand.Intn(100)
	fmt.Println("a =", a)

	p := getPrime()
	g := rand.Intn(100)

	pw := math.Pow(float64(g), float64(a))
	aliceA := math.Mod(pw, float64(p))

	postData, err := sendRequest(p, g, 0)
	bobB := postData.P3

	fmt.Println("Публичный ключ Боба: ", bobB)

	postData, err = sendRequest(0, 0, aliceA)

	pw = math.Pow(bobB, float64(a))
	K := math.Mod(pw, float64(p))
	fmt.Println("K =", K)

	return err
}

func main() {
	step1 := sendPg()
	fmt.Printf("%t\n", step1)
}