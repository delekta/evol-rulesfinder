from textwrap import dedent

def embed_code(code):
    return dedent('''
      <script>var enchant = enchant || []</script>
      <script src="//platform.enchant.com" data-enchant-messenger-id="{code}" async></script>
    ''').format(code=code)
