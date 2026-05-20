from byte.intrinsics import intrinsic, IntrinsicClass, IntrinsicCallContext
from byte.llvm_extensions import llint
from byte import ast


class StringBuilder(IntrinsicClass):
    def init(self):
        int_type = self.file.type_map.get('int')
        string_type = self.file.type_map.get('string')
        pointer_type = self.file.type_map.get('pointer')
        nil_type = self.file.type_map.get('nil')
        
        @intrinsic(
            self, self._type, [ast.Param(ast.Position(), int_type, 'capacity')],
            flags=ast.FunctionFlags(static=True, method=True)
        )
        def _new(ctx: IntrinsicCallContext):
            malloc = ctx.module.registry.get('malloc')

            capacity = ctx.arg(0)

            buf = ctx.builder.call(malloc, [capacity], 'buf')
            # TODO: check if NULL

            StringBuilder_type = ctx.module.context.get_identified_type('StringBuilder')
            return ctx.builder.struct(StringBuilder_type, [buf, llint(0), capacity], 'StringBuilder')

        @intrinsic(
            self, nil_type, [ast.Param(ast.Position(), self._type.reference(), 'self')],
            flags=ast.FunctionFlags(method=True)
        )
        def _destroy(ctx: IntrinsicCallContext):
            free = ctx.module.registry.get('free')
            
            struct = ctx.arg(0)

            buf_ptr = ctx.builder.extract_ptr(struct, 0, 'buf.ptr')
            ctx.builder.call(free, [ctx.builder.load(buf_ptr, 'buf')])

        @intrinsic(
            self, nil_type, [
                ast.Param(ast.Position(), self._type.reference(), 'self'), ast.Param(ast.Position(), string_type, 'value')
            ], flags=ast.FunctionFlags(method=True)
        )
        def _add(ctx: IntrinsicCallContext):
            realloc = ctx.module.registry.get('realloc')
            memcpy = ctx.module.registry.get('memcpy')

            struct = ctx.arg(0)
            
            value_length = ctx.call('string.length', [ctx.args[1]])
            buf_ptr = ctx.builder.extract_ptr(struct, 0, 'buf.ptr')
            length_ptr = ctx.builder.extract_ptr(struct, 1, 'length.ptr')
            capacity_ptr = ctx.builder.extract_ptr(struct, 2, 'capacity.ptr')

            length = ctx.builder.load(length_ptr, 'length')
            new_length = ctx.builder.add(length, value_length, 'new_length')
            capacity = ctx.builder.load(capacity_ptr, 'capacity')
            needs_resize = ctx.builder.icmp_signed('>=', new_length, capacity, 'needs_resize')
            with ctx.builder.if_then(needs_resize):
                new_capacity = ctx.builder.mul(capacity, llint(2), 'new_capacity')
                buf = ctx.builder.load(buf_ptr, 'buf')
                new_buf = ctx.builder.call(realloc, [buf, new_capacity], 'new_buf')
                # TODO: check if NULL
                
                ctx.builder.store(new_buf, buf_ptr)
                ctx.builder.store(new_capacity, capacity_ptr)
            
            value_ptr = ctx.call('string.ptr', [ctx.args[1]])
            buf = ctx.builder.load(buf_ptr, 'buf')
            buf_offset = ctx.builder.gep(buf, [length], True, 'buf_offset')
            ctx.builder.call(memcpy, [buf_offset, value_ptr, value_length, llint(0, 1)])
            ctx.builder.store(new_length, length_ptr)

        @intrinsic(self, string_type, [ast.Param(ast.Position(), self._type, 'self')], flags=ast.FunctionFlags(method=True))
        def _to_string(ctx: IntrinsicCallContext):
            struct = ctx.arg(0)

            ptr = ctx.builder.extract_value(struct, 0, 'ptr')
            length = ctx.builder.extract_value(struct, 1, 'length')
            return ctx.call('string.new.pointer.int', [
                ast.Arg(ctx.pos, pointer_type, ptr),
                ast.Arg(ctx.pos, int_type, length)
            ])
