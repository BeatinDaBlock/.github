<?php
/**
 * Footer template
 */
?>
<footer class="footer">
  <div class="footer__inner">
    <p class="footer__brand">
      © 2012–<?php echo esc_html( current_time( 'Y' ) ); ?> BeatinDaBlock. All rights reserved.
    </p>
    <?php
      wp_nav_menu( [
          'theme_location' => 'footer',
          'container'      => false,
          'menu_class'     => 'footer__links',
          'fallback_cb'    => function () {
              echo '<ul class="footer__links">
                <li><a href="' . esc_url( get_bloginfo( 'rss2_url' ) ) . '">RSS Feed</a></li>
                <li><a href="' . esc_url( home_url( '/contact/' ) ) . '">Contact</a></li>
                <li><a href="https://github.com/Cybersoulja">GitHub</a></li>
              </ul>';
          },
      ] );
    ?>
  </div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
