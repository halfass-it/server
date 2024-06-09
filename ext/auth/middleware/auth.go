package middleware

import (
	"fmt"
	"os"
	"net/url"
	"time"
	"github.com/auth0/go-jwt-middleware/v2"
	"github.com/auth0/go-jwt-middleware/v2/jwks"
	"github.com/auth0/go-jwt-middleware/v2/validator"
	"github.com/gin-gonic/gin"
)

func AuthenticationMiddleware (ctx *gin.Context) {



	token, err := jwtmiddleware.AuthHeaderTokenExtractor(ctx.Request)
	if err != nil {
		ctx.String(401, "Failed to extract token.")
		return
	}

	issuerUrl, err := url.Parse("https://" + os.Getenv("AUTH0_DOMAIN") + "/")
	if err != nil  {
		fmt.Printf("This is issuer url: %s", err)
		ctx.String(500, "Failed to parse issuer URL.")
		return
	}

	provider := jwks.NewCachingProvider(issuerUrl, 5 * time.Minute)

	jwtValidator, err := validator.New(
		provider.KeyFunc,
		validator.RS256,
		issuerUrl.String(),
		[]string{os.Getenv("AUTH0_AUDIENCE")},
	)
	if err != nil {
		fmt.Printf("This is jwt validator: %s", err)
		ctx.String(500, "Failed to create JWT validator.")
		return
	}

	valid, err := jwtValidator.ValidateToken(ctx.Request.Context(), token)
	if err != nil {
		fmt.Printf("This is validate token: %s", err)
		ctx.String(500, "Failed to validate token.")
		return
	}

	if valid != nil {
		ctx.Next()
		return
	}
}

func AuthorizationMiddleware (ctx *gin.Context) {
	//Find way of JWT have permissions inside the token
	ctx.Next()
}