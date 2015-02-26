/**
 * Pull SMC statistics
 */

var smc_stats = {
  users: 0,
  proj: 0,
  proj24: 0,

  init: function () {
    console.log("smc_statistics.init");
    smc_stats.users = $("#status-users");
    smc_stats.proj = $("#status-projects");
    smc_stats.proj24 = $("#status-24h");
    smc_stats.run();
  },
  run: function () {
    // $.getJSON("http://localhost:8080/stats")
    $.getJSON("http://www.sagemath.com/stats")
        .done(function (data) {
          console.log("smc stats: success", data);
          var nbusers = 0;
          $(data["hub_servers"]).each(
              function(i, x){
                nbusers += x["clients"];
              }
          );
          smc_stats.users.text(nbusers);
          smc_stats.proj.text(data["active_projects"]);
          smc_stats.proj24.text(data["last_day_projects"]);
        })
        .fail(function (data) {
          console.log("smc stats: error:", data);
        })
        .always(function() {
          setTimeout(smc_stats.run, 10000);
        });
  }
};

$(smc_stats.init);
