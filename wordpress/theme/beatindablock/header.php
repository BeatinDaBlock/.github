<?php
/**
 * Header template
 */
?><!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
  <meta charset="<?php bloginfo( 'charset' ); ?>" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<nav class="nav">
  <div class="nav__inner">
    <a class="nav__logo" href="<?php echo esc_url( home_url( '/' ) ); ?>">
      BeatinDaBlock
    </a>
    <?php
      wp_nav_menu( [
          'theme_location' => 'primary',
          'container'      => false,
          'menu_class'     => 'nav__links',
          'fallback_cb'    => function () {
              echo '<ul class="nav__links">
                <li><a href="' . esc_url( home_url( '/' ) ) . '">Home</a></li>
                <li><a href="' . esc_url( get_post_type_archive_link( 'episode' ) ) . '">Episodes</a></li>
                <li><a href="' . esc_url( home_url( '/about/' ) ) . '">About</a></li>
                <li><a href="' . esc_url( home_url( '/blog/' ) ) . '">Blog</a></li>
                <li><a href="' . esc_url( home_url( '/contact/' ) ) . '">Contact</a></li>
              </ul>';
          },
      ] );
    ?>
  </div>
</nav>
