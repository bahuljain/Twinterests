var network, nodes, edges;

function loadGraph(N,E, fixed, nodeShape, nodeSize, improvedLayout) {
  if (!improvedLayout) {
    N = addPositions(N);  
  }
  
  nodes = new vis.DataSet(N);

  // create an array with edges
  edges = new vis.DataSet(E);

  // create a network
  var container = document.getElementById('mynetwork');

  var data = {
    nodes: nodes,
    edges: edges
  };

  var options = {
    autoResize: false,
    height: '100%',
    width: '100%',
    clickToUse: false,
    edges: {
      color: {
        color: 'rgba(0,0,0,0.1)',
        highlight: 'rgba(0,0,0,0.7)',
      },
      dashes: false,
      shadow: false,
      width: 1,
      hoverWidth: 2,
    },
    nodes: {
      fixed: fixed,
      borderWidth: 3,
      borderWidthSelected: 6,
      size: nodeSize,
      color: {
        background: 'rgba(20,20,20,1)',
        border: 'rgba(0,0,0,0.5)',
        highlight: 'black',
      },
      shape: nodeShape,
      shadow: true
    },
    physics: {
      enabled: true,
      stabilization: true,
    },
    manipulation: {
      enabled: false,
      editEdge: false,
    },
    interaction: {
      hover: false,
      hoverConnectedEdges: false,
    },
    layout: {
      improvedLayout: improvedLayout,
      hierarchical: {
        enabled: false,
        levelSeparation: 10,
        direction: 'LR',   // UD, DU, LR, RL
      }
    } 
  };
  network = new vis.Network(container, data, options);  
}

function addPositions(N) {
  var w = window.innerWidth;
  var h = window.innerHeight;

  console.log(w);
  console.log(h);

  
  var radiusY = 350;
  var radiusX = 600;

  var n = N.length;
  var delta = 2 * Math.PI / n;


  for (var i = 0; i < n; i++) {
    N[i].x = false;
    N[i].x = Math.random() * 1200 + 40;

    N[i].y = false;
    N[i].y = Math.random() * 700 + 50;
  }    

  return N
}
