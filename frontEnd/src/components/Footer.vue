<template>
  <div class="footer-content">
    <div class="footer-copy">
      &#169; 2020
      <br>
      <a
        href="https://github.com/mrutherfoord/"
        noopener
        noreferrer
        target="_blank"
        class="mel-link"
      >
        Melissa Rutherfoord
      </a>
      <br>
      <a
        href="https://github.com/bradleyhop/"
        noopener
        noreferrer
        target="_blank"
      >
        Bradley Smith
      </a>
      <br>
      <a
        href="https://github.com/mrutherfoord/AIC-Photo-Match"
        noopener
        noreferrer
        target="_blank"
      >
        Project GitHub
      </a>
      <br>
    </div>
  </div>
</template>

<style lang="scss">
.footer-content {
  background-color: #e0e0e0;
  font-size: 0.9rem;
  height: 6.5rem;
  margin: 3rem 0 0 0;
  padding: 1rem;
  text-align: left;
  width: 100%;
}

.footer-copy {
  float: right;
  line-height: 1.2rem;
  margin-right: 1rem;

  & a {
    color: inherit;
    text-decoration: none;
  }

  & a:hover {
    text-decoration: underline;
  }

  & a:active {
    color: #fff;
  }
}
</style>
