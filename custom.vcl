/**
 * This is based on the fastly-boilerplate.vcl - to see the differences run:
 *
 *    diff -u fastly-boilerplate.vcl custom.vcl
 */
${custom_vcl_backends}
sub vcl_recv {
#FASTLY recv

  ${custom_vcl_recv}
  if (! req.http.fastly-ff) {

    # Adds X-Client-IP header
    set req.http.X-Client-IP = req.http.Fastly-Client-IP;
    
    ${custom_vcl_recv_no_shield}
  }
  if (req.http.fastly-ff) {
    ${custom_vcl_recv_shield_only}
  }

  if (req.request != "HEAD" && req.request != "GET" && req.request != "FASTLYPURGE") {
    return(pass);
  }

  return(${vcl_recv_default_action});
}

sub vcl_fetch {
#FASTLY fetch

  if ((beresp.status == 500 || beresp.status == 503) && req.restarts < 1 && (req.request == "GET" || req.request == "HEAD")) {
    restart;
  }

  if (req.restarts > 0) {
    set beresp.http.Fastly-Restarts = req.restarts;
  }

  if (beresp.http.Set-Cookie) {
    set req.http.Fastly-Cachetype = "SETCOOKIE";
    return(pass);
  }

  if (beresp.http.Cache-Control ~ "private|no-cache") {
    set req.http.Fastly-Cachetype = "PRIVATE";
    return(pass);
  }

  if (beresp.status == 500 || beresp.status == 503) {
    set req.http.Fastly-Cachetype = "ERROR";
    set beresp.ttl = 1s;
    set beresp.grace = 5s;
    return(deliver);
  }

  if (beresp.http.Expires || beresp.http.Surrogate-Control ~ "max-age" || beresp.http.Cache-Control ~ "(s-maxage|max-age)") {
    # keep the ttl here
  } else {
    # apply the default ttl
    set beresp.ttl = 3600s;
  }

  return(deliver);
}

sub vcl_hit {
#FASTLY hit

  if (!obj.cacheable) {
    return(pass);
  }
  return(deliver);
}

sub vcl_miss {
#FASTLY miss
  return(fetch);
}

sub vcl_deliver {
#FASTLY deliver

  ${custom_vcl_deliver}

  return(deliver);
}

sub vcl_error {
#FASTLY error

 /* handle proxy errors */
 if (obj.status == 502 || obj.status == 503) {
   synthetic {"${proxy_error_response}"};
   return(deliver);
 }

  ${custom_vcl_error}
}

sub vcl_pass {
#FASTLY pass
}

sub vcl_log {
#FASTLY log
}
