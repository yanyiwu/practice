package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"os"
	"path"
	"strings"

	"github.com/blevesearch/bleve"
	_ "github.com/yanyiwu/gojieba/bleve"
)

var dictdir = flag.String("dictdir", path.Join(os.Getenv("GOPATH"), "src/github.com/yanyiwu/gojieba/dict"), "")
var dictpath = flag.String("dictpath", path.Join(*dictdir, "jieba.dict.utf8"), "")
var hmmpath = flag.String("hmmpath", path.Join(*dictdir, "hmm_model.utf8"), "")
var userdictpath = flag.String("userdictpath", path.Join(*dictdir, "user.dict.utf8"), "")

var dir = flag.String("dir", "blog/_posts", "")

func ListDir(dirPth string, suffix string) (files []string) {
	files = make([]string, 0, 10)
	dir, err := ioutil.ReadDir(dirPth)
	if err != nil {
		panic(err)
	}
	suffix = strings.ToUpper(suffix)
	for _, fi := range dir {
		if fi.IsDir() {
			continue
		}
		if strings.HasSuffix(strings.ToUpper(fi.Name()), suffix) {
			files = append(files, path.Join(dirPth, fi.Name()))
		}
	}
	return files
}

type Doc struct {
	Title   string
	Content string
	Url     string
}

func ParseToUrl(file string) string {
	basename := path.Base(file)
	segs := strings.SplitN(basename, "-", 4)
	url := strings.Join(segs, "/")
	return url
}

func ParseToDoc(file string) Doc {
	metamap := make(map[string]string, 0)
	content := ""
	url := ParseToUrl(file)
	f, err := os.Open(file)
	if err != nil {
		panic(err)
	}
	defer f.Close()
	reader := bufio.NewReader(f)
	cnt := 0
	for {
		line, err := reader.ReadString('\n')
		if err != nil {
			break
		}
		line = strings.TrimSpace(line)
		if cnt < 2 && strings.HasPrefix(line, "---") {
			cnt++
		}
		if cnt == 1 {
			segs := strings.SplitN(line, ":", 2)
			if len(segs) == 2 {
				key, value := segs[0], segs[1]
				metamap[key] = strings.Trim(value, "\" ")
			}
		}
		if cnt == 2 {
			content += line
		}
	}
	title := metamap["title"]
	category := metamap["category"]
	url = path.Join("/", category, url)
	url = strings.Replace(url, ".md", ".html", 1)
	url = strings.Replace(url, ".markdown", ".html", 1)
	doc := Doc{
		Url:     url,
		Title:   title,
		Content: content,
	}
	return doc
}

func main() {
	files := ListDir(*dir, ".md")
	docs := make([]Doc, 0, len(files))
	for _, file := range files {
		docs = append(docs, ParseToDoc(file))
	}

	indexMapping := bleve.NewIndexMapping()
	dir := "blog.index"
	os.RemoveAll(dir)

	err := indexMapping.AddCustomTokenizer("gojieba",
		map[string]interface{}{
			"dictpath":     *dictpath,
			"hmmpath":      *hmmpath,
			"userdictpath": *userdictpath,
			"type":         "gojieba",
		},
	)
	if err != nil {
		panic(err)
	}
	err = indexMapping.AddCustomAnalyzer("gojieba",
		map[string]interface{}{
			"type":      "gojieba",
			"tokenizer": "gojieba",
		},
	)
	if err != nil {
		panic(err)
	}
	indexMapping.DefaultAnalyzer = "gojieba"

	index, err := bleve.New(dir, indexMapping)
	if err != nil {
		panic(err)
	}
	for _, doc := range docs {
		if err := index.Index(doc.Url, doc); err != nil {
			panic(err)
		}
	}

	querys := []string{
		"中文分词",
		"推荐系统",
		"选择",
	}

	for _, q := range querys {
		req := bleve.NewSearchRequest(bleve.NewQueryStringQuery(q))
		req.Highlight = bleve.NewHighlight()
		res, err := index.Search(req)
		if err != nil {
			panic(err)
		}
		x, err := json.Marshal(res)
		if err != nil {
			panic(err)
		}
		fmt.Println(string(x))
	}
}
