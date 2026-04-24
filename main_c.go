package main

/*
#include <stdlib.h>
*/
import "C"

import (
	"dirp/pkg/dirp"
	"encoding/json"
	"unsafe"
)

type cNode struct {
	Name     string  `json:"name"`
	Children []cNode `json:"children,omitempty"`
}

type cError struct {
	Code     string `json:"code,omitempty"`
	Category string `json:"category,omitempty"`
	Message  string `json:"message"`
	Pos      int    `json:"pos,omitempty"`
	Line     int    `json:"line,omitempty"`
	Col      int    `json:"col,omitempty"`
}

type cResponse struct {
	OK    bool    `json:"ok"`
	Nodes []cNode `json:"nodes,omitempty"`
	Error *cError `json:"error,omitempty"`
}

func nodesToJSON(nodes []*dirp.Node) []cNode {
	out := make([]cNode, 0, len(nodes))
	for _, n := range nodes {
		item := cNode{Name: n.Name}
		if len(n.Children) > 0 {
			item.Children = nodesToJSON(n.Children)
		}
		out = append(out, item)
	}
	return out
}

func makeError(err error, input string) *cError {
	withPos := dirp.WithLineCol(err, input)
	if de, ok := dirp.AsError(withPos); ok {
		return &cError{
			Code:     de.Code.String(),
			Category: de.Code.Category(),
			Message:  de.Msg,
			Pos:      de.Pos,
			Line:     de.Line,
			Col:      de.Col,
		}
	}
	return &cError{Message: err.Error()}
}

func toCString(v any) *C.char {
	b, err := json.Marshal(v)
	if err != nil {
		return C.CString(`{"ok":false,"error":{"message":"json marshal failed"}}`)
	}
	return C.CString(string(b))
}

//export ParseDirpJSON
func ParseDirpJSON(dsl *C.char) *C.char {
	goDSL := C.GoString(dsl)
	nodes, err := dirp.Parse(goDSL)
	if err != nil {
		return toCString(cResponse{
			OK:    false,
			Error: makeError(err, goDSL),
		})
	}
	return toCString(cResponse{
		OK:    true,
		Nodes: nodesToJSON(nodes),
	})
}

//export BuildDirpFromDSLJSON
func BuildDirpFromDSLJSON(root *C.char, dsl *C.char) *C.char {
	goRoot := C.GoString(root)
	goDSL := C.GoString(dsl)

	nodes, err := dirp.Parse(goDSL)
	if err != nil {
		return toCString(cResponse{
			OK:    false,
			Error: makeError(err, goDSL),
		})
	}
	if err := dirp.Build(goRoot, nodes); err != nil {
		return toCString(cResponse{
			OK:    false,
			Error: &cError{Message: err.Error()},
		})
	}
	return toCString(cResponse{OK: true})
}

//export FreeCString
func FreeCString(p *C.char) {
	C.free(unsafe.Pointer(p))
}

func main() {}
