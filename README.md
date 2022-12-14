

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/gmagno/igl">
    <img src="./nbweb/public/splash_logo.svg" alt="Logo" width="256" height="256">
  </a>

  <h3 align="center">nbapp</h3>

  <p align="center">
    A generator of Newton Basins fractals
    <br />
    <a href=""><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="">View Demo</a> :construction:
    ·
    <a href="https://github.com/MagnoBrothers/nbapp/issues">Report Bug</a>
    ·
    <a href="https://github.com/MagnoBrothers/nbapp/issues">Request Feature</a>
  </p>
</p>


# Running nbapp locally

Create the following .env files:

- `.envs/.local/.api`
- `.envs/.local/.api.test`
- `.envs/.local/.web`

For reference use the `.envs/.local/.*.example` files.


Install `docker` and execute:

```sh
make restart
```

Then follow [http://127.0.0.1:3000](http://127.0.0.1:3000)