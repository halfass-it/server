package models

import (
	"gorm.io/gorm"
)

type User struct {
	gorm.Model
	Name string 
	Email string 
	JwtToken string 
	ClientID int 
	IsClientManager bool
}

type Client struct {
	gorm.Model
	Name string
}