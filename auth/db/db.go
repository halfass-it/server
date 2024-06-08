package db

import (
	"encoding/json"
	"os"
	"fmt"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

type LocalDb struct {
	LocalDbUrl string `json:"localDb"`
}

func getEnvDb() (string, error)  {
	file, err := os.Open("env.json")
	if err != nil {
		fmt.Println(err)
		return "", err
	}
	var localDb LocalDb
	decoder := json.NewDecoder(file)
	if err := decoder.Decode(&localDb); err != nil {
		fmt.Println(err)
		return "", err
	}
	var dbUrl = localDb.LocalDbUrl
	file.Close()
	return dbUrl, nil
}

func Connect() (*gorm.DB, error) {
	dbUrl, err := getEnvDb()
	if err != nil {
		return nil, err
	}
	db, err := gorm.Open(postgres.Open(dbUrl), &gorm.Config{})
	if err != nil {
		panic("Failed to connect to database!")
	}
	return db, nil	
}