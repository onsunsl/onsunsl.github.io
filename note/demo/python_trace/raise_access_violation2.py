

for exc in (
        0x00000000,
        0x34567890,
        0x40000000,
        0x40001000,
        0x70000000,
        0x7FFFFFFF,
):
    output, exitcode = self.get_output(f"""
                import faulthandler
                faulthandler.enable()
                faulthandler._raise_exception(0x{exc:x})
                """
                                       )