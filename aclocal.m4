AC_DEFUN([PY_CHECK_INTERPRETER], [
    py_version=`$1 -V 2>&1 | grep -o '[[0-9]]\.[[0-9]]\.[[0-9]]'`
    AS_ECHO_N(["checking version of $1... "])
    AS_VERSION_COMPARE([$py_version], [$2], 
        [
            AS_ECHO(["$py_version < $2"])
        ], 
        [
            AS_ECHO(["$py_version = $2"])
        ], 
        [
            AS_ECHO(["$py_version > $2 OK"]),
            AC_SUBST([PYTHON3_BIN], [$1])
        ]
    )
])

AC_DEFUN([PY_FIND_INTERPRETER], [
    for interpreter in \
        /usr/bin/python \
        /usr/local/bin/python \
        /usr/bin/python3 \
        /usr/bin/python34 \
        /usr/bin/python3.6
    do
        AS_IF([test -x $interpreter],
            [
                PY_CHECK_INTERPRETER([$interpreter], [$1])
            ]
        )
    done

])
