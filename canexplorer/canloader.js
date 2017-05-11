function p(x) {
  console.log(x);
}

var msgs = {};

function update_graph(bstart, bend, $scope) {
  var tmsg = msgs[$scope.selectedName];
  var vals = [];
  var str = "time,value\n";
  p(bstart);
  p(bend);
  for (var i = 0; i < tmsg.length; i++) {
    var uint = Uint64BE(tmsg[i][1]);

    // slow!
    var tt = "0"+uint.toString(2);
    tt = tt.substring(0, tt.length - (63-bend))
    tt = tt.substring(tt.length - (bend-bstart) - 1)
    var nn = parseInt(tt, 2);

    str += tmsg[i][0]+","+nn+"\n";
    vals.push(nn);
  }
  p(vals);

  g2 = new Dygraph(
    document.getElementById("graph"),
    str,
    {});
}

function load_can_for_part(base, num, $scope) {
  var urls = [base+"/Log/"+num+"/can/t",
              base+"/Log/"+num+"/can/src",
              base+"/Log/"+num+"/can/address",
              base+"/Log/"+num+"/can/data"];
  return Promise.all(urls.map(NumpyLoader.promise)).then(function(da) {
    p(da);
    for (var i = 0; i < da[0].data.length; i++) {
      var t = da[0].data[i];
      var src = Int64LE(da[1].data, i*8).toString(10);
      var address = Int64LE(da[2].data, i*8).toString(16);
      var id = src + ":" + address;
      var data = da[3].data.slice(i*8, (i+1)*8);
      if (msgs[id] === undefined) msgs[id] = [];
      msgs[id].push([t, data]);
    }
    p(msgs);

    // handle update to parse msgs
    $scope.update = function() {
      var tmsg = msgs[$scope.selectedName];
      $scope.tmsg = tmsg.slice(0, 10);
      // apply not needed here
    };

    $scope.select = function(msg) {
      p(msg);
      $scope.mm = msg[1];
    };

    $scope.bselect = function(i, j) {
      p(i+" "+j);
      $scope
      if ($scope.firstSelect) {
        $scope.bstart = 8*i + (7-j);
        $scope.bend = -1;
        $scope.firstSelect = false;
      } else {
        $scope.bend = 8*i + (7-j);
        $scope.firstSelect = true;
        update_graph($scope.bstart, $scope.bend, $scope);
      }
      p($scope.bstart + " " + $scope.bend);
    };

    $scope.names = Object.keys(msgs).sort();
    $scope.$apply();
  });
}


var app = angular.module('myApp', []);
var queryDict = {};

app.controller('myCtrl', function($scope) {
  location.search.substr(1).split("&").forEach(function(item) {queryDict[item.split("=")[0]] = item.split("=")[1]});

  //$scope.names = msgs;
  var parts = [];
  for (var i = 0; i < parseInt(queryDict['max']); i++) parts.push(i);
  p(parts);
  $scope.parts = parts;

  $scope.h2 = function(x) {
    var ret = x.toString(16);
    if (ret.length == 1) ret = "0"+ret;
    return ret;
  }
  $scope.gb = function(m, j) {
    return (m >> j) & 1;
  }

  $scope.bstart = 0;
  $scope.bend = -1;
  $scope.firstSelect = true;

  $scope.selectedPart = '0';
  $scope.updateall = function() {
    msgs = {};
    load_can_for_part(queryDict['url'], parseInt($scope.selectedPart), $scope)
  };
  $scope.updateall();
});


