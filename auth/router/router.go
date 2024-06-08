package router

import (
	// "net/http"
	// "fmt"
	"github.com/gin-gonic/gin"
)

func AddRoutes (service *gin.Engine) *gin.Engine {
	service.GET("/", func(ctx *gin.Context) {})
	service.POST("/", func (ctx *gin.Context)  {})
	service.DELETE("/", func (ctx *gin.Context)  {})
	service.PUT("/", func (ctx *gin.Context)  {})
	return service
}