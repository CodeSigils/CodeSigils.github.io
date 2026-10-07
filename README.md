# Code Sigils

Personal blog on technology, programming, AI tools, books, tutorials, and whatever catches my interest.

## About

A personal knowledge base documenting tools, techniques, and experimentation
in software development. Built with [Zensical](https://zensical.org) and hosted
on GitHub Pages.

## License

[MIT License](LICENSE) - Copyright 2026 Tom Geo

## Disclaimer

This site contains personal opinions, research, and experimental notes.

**The author is not responsible for any loss of data, system damage, or other issues arising from following the content here.**

> **Reader Beware**
> - Verify all commands against official documentation before running
> - Understand code before execution
> - Always back up data before making system changes
> - Your experience may differ from mine

See [disclaimer docs page](./docs/disclaimer.md) for full details.

## Local Development

```bash
# Sync the locked build environment (UV installs Python 3.13 when needed)
uv sync --locked

# Build the site
uv run zensical build --clean

# Serve locally
uv run zensical serve
```

## Contributing

This is a personal documentation site. Feel free to fork and adapt patterns for your own projects.
