package main

import (
	"fmt"
	"log"

	"sync"

	"github.com/yanyiwu/gojieba"
)

func main() {
	const (
		JIEBA_DICT_PATH       = "jieba/dict/jieba.dict.utf8"
		JIEBA_HMM_PATH        = "jieba/dict/hmm_model.utf8"
		JIEBA_USER_DICT_PATH  = "jieba/dict/user.dict.utf8"
		JIEBA_IDF_PATH        = "jieba/dict/idf.utf8"
		JIEBA_STOP_WORDS_PATH = "jieba/dict/stop_words.utf8"
	)

	log.Println("加载jieba词库...")
	jieba_segmenter := gojieba.NewJieba(JIEBA_DICT_PATH, JIEBA_HMM_PATH, JIEBA_USER_DICT_PATH)
	defer jieba_segmenter.Free()

	wt := &sync.WaitGroup{}

	desc := "测试测试测试测试测试测试"

	for j := 0; j < 1; j++ {
		wt.Add(1)
		go func() {
			//for i := 0; i < 2000000000; i++ {
			for i := 0; i < 1600000; i++ {
				fmt.Println(i)
				jieba_segmenter.Cut(desc, true)
			}
			wt.Done()
		}()
	}

	wt.Add(1)
	wt.Wait()
}
