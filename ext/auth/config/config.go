package config

import (
	"fmt"
	"usr_mgmnt_auth/main/middleware"
	"usr_mgmnt_auth/main/router"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func SetupRouter(config cors.Config) *gin.Engine {

	service := gin.Default()

	service.Use(cors.New(config))
	service.Use(middleware.AuthenticationMiddleware)
	service.Use(middleware.AuthorizationMiddleware)

	gateway := router.AddRoutes(service)

	return gateway
}

func SetupCorsConfig(auth0Port string) cors.Config {

	config := cors.DefaultConfig()
	config.AllowOrigins = []string{fmt.Sprintf("http://localhost:%s", auth0Port)}
	config.AllowMethods = []string{"GET", "POST", "PUT", "DELETE"}
	config.AllowHeaders = []string{"Origin", "Content-Type", "Authorization"}

	return config
}
