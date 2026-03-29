; ModuleID = "test"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

%"string" = type {i8*, i32}
declare external void @"string.destroy"(%"string" %".1")

declare external %"string" @"string.new"(i8* %".1", i32 %".2")

define i32 @"main"()
{
entry:
  %"str.ptr" = getelementptr inbounds [12 x i8], [12 x i8]* @"str", i32 0, i32 0
  %"string.new" = call %"string" @"string.new"(i8* %"str.ptr", i32 11)
  %"_0.addr" = alloca %"string"
  store %"string" %"string.new", %"string"* %"_0.addr"
  %"_0" = load %"string", %"string"* %"_0.addr"
  %"s.addr" = alloca %"string"
  store %"string" %"_0", %"string"* %"s.addr"
  %"s" = load %"string", %"string"* %"s.addr"
  %"string_fmt_ptr" = getelementptr inbounds [4 x i8], [4 x i8]* @"string_fmt", i32 0, i32 0
  %"s_ptr" = extractvalue %"string" %"s", 0
  call void (i8*, ...) @"printf"(i8* %"string_fmt_ptr", i8* %"s_ptr")
  %"s.1" = load %"string", %"string"* %"s.addr"
  call void @"string.destroy"(%"string" %"s.1")
  ret i32 0
}

@"str" = internal constant [12 x i8] c"Hello world\00"
declare external void @"printf"(i8* %".1", ...)

@"string_fmt" = internal constant [4 x i8] c"%s\0a\00"