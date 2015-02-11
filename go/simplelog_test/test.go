package main

import (
	log "github.com/yanyiwu/simplelog"
)

func main() {
	log.Debug("hello simplelog.")
	log.Info("hello simplelog.")
	log.Warn("hello simplelog.")
	log.Error("hello simplelog.")
	log.Fatal("hello simplelog.")
	log.SetLevel(log.LEVEL_FATAL)
	log.Debug("hello simplelog.")
	log.Info("hello simplelog.")
	log.Warn("hello simplelog.")
	log.Error("hello simplelog.")
	log.Fatal("hello simplelog.")
}
