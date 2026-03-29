; ModuleID = "builtins"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

%"string" = type {i8*, i32}
define void @"string.destroy"(%"string" %"param.s")
{
param_allocation:
  %"s.addr" = alloca %"string"
  store %"string" %"param.s", %"string"* %"s.addr"
  br label %"entry"
entry:
  %"s" = load %"string", %"string"* %"s.addr"
  %"string.ptr" = extractvalue %"string" %"s", 0
  call void @"free"(i8* %"string.ptr")
  ret void
}

declare external void @"free"(i8* %".1")

define %"string" @"string.new"(i8* %"param.ptr", i32 %"param.length")
{
param_allocation:
  %"ptr.addr" = alloca i8*
  store i8* %"param.ptr", i8** %"ptr.addr"
  %"length.addr" = alloca i32
  store i32 %"param.length", i32* %"length.addr"
  br label %"entry"
entry:
  %"length" = load i32, i32* %"length.addr"
  %"+.int.int" = add i32 %"length", 1
  %"malloc" = call i8* @"malloc"(i32 %"+.int.int")
  %"ptr_copy.addr" = alloca i8*
  store i8* %"malloc", i8** %"ptr_copy.addr"
  %"ptr_copy" = load i8*, i8** %"ptr_copy.addr"
  %"ptr" = load i8*, i8** %"ptr.addr"
  %"length.1" = load i32, i32* %"length.addr"
  call void @"memcpy"(i8* %"ptr_copy", i8* %"ptr", i32 %"length.1")
  %"ptr_copy.1" = load i8*, i8** %"ptr_copy.addr"
  %"length.2" = load i32, i32* %"length.addr"
  %"null_terminate" = getelementptr inbounds i8, i8* %"ptr_copy.1", i32 %"length.2"
  store i8 0, i8* %"null_terminate"
  %"ptr_copy.2" = load i8*, i8** %"ptr_copy.addr"
  %"length.3" = load i32, i32* %"length.addr"
  %"string_struct" = insertvalue %"string" undef, i8* %"ptr_copy.2", 0
  %"string_struct.1" = insertvalue %"string" %"string_struct", i32 %"length.3", 1
  %"_0.addr" = alloca %"string"
  store %"string" %"string_struct.1", %"string"* %"_0.addr"
  %"_0" = load %"string", %"string"* %"_0.addr"
  ret %"string" %"_0"
}

declare external i8* @"malloc"(i32 %".1")

declare external void @"memcpy"(i8* %".1", i8* %".2", i32 %".3")
