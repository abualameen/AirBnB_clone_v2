# 101-setup_web_static.pp

# Install Nginx package
package { 'nginx':
  ensure => 'installed',
}

# Create necessary directories
file { '/data':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Create a fake HTML file for testing
file { '/data/web_static/releases/test/index.html':
  content => '<html>\n\t<head>\n\t</head>\n\t<body>\n\t\tHolberton School\n\t</body>\n</html>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test/',
  force  => true,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Use sed to modify Nginx configuration
exec { 'update_nginx_config':
  command => "sed -i 's#server_name _;#server_name _;\\n\\tlocation /hbnb_static {\\n\\t\\talias /data/web_static/current/;\\n\\t}\\n#' /etc/nginx/sites-available/default",
  path    => '/usr/bin',
  require => Package['nginx'],
}

# Restart Nginx service
service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => Exec['update_nginx_config'],
}
