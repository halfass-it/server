package auth

import (
	"fmt"
	"halfass-it/server/auth/db"
	"halfass-it/server/auth/models"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
)

func main() {

	port, exists := os.LookupEnv("PORT")
	if !exists {
		port = "8080"
	}

	DB, err := db.Connect()
	if err != nil {
		panic(err)
	}
	DB.AutoMigrate(&models.User{}, &models.Client{})

	service := gin.Default()

	service.GET("/", func(ctx *gin.Context) {
		ctx.JSON(http.StatusOK, gin.H{
			"message": "Service is running buddy",
		})
	})
	service.Run(fmt.Sprintf(":%s", port))
}
