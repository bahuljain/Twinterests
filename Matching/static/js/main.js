var network, nodes, edges;

function loadGraph(N,E) {
  // N = addPositions(N);

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
      fixed: false,
      borderWidth: 3,
      borderWidthSelected: 6,
      size: 20,
      color: {
        background: 'rgba(20,20,20,1)',
        border: 'rgba(0,0,0,0.5)',
        highlight: 'black',
      },
      shape: 'circularImage',
      shadow: true
    },
    physics: {
      enabled: false,
      stabilization: false,
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
      improvedLayout: true,
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

// function modifyGraph(){
//   selectedEdges = network.getSelectedEdges();

//   for (id in edges._data) {
//     console.log(typeof(id))
//     if (selectedEdges.indexOf(id) > -1) {
//       // console.log('true');
//       edges.update({id:id, hidden:true});
//     } else {
//       // console.log('false');
//       edges.update({id:id, hidden:false});
//     }
    
//   }
// }
