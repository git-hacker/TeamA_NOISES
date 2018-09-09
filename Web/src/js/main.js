$(document).ready(load)

function load() {
  var wave = null,
    transformWave = null,
    sWave = null,
    id = '',
    baseUrl = 'http://localhost:60000',
    wave1 = null

  getList()

  $('.sideBar').bind('click', createWave)

  $('#play').bind('click', playIn)

  $('#transform').bind('click', transformVocie)

  $('#playOut').bind('click', playOut)

  $('#ai').bind('click', transformVocieFromAi)

  function createWave(e) {
    if (
      $(e.target)
        .attr('class')
        .indexOf('active') !== -1
    )
      return

    $('#wave-modal').removeClass('active');
    $('#wave-modal').addClass('active');
    const url = $(e.target).attr('data-url')

    id = $(e.target).attr('data-id')

    $('.item').removeClass('active')
    $(e.target).addClass('active')

    if (!wave) {
      wave = new CreateWave('#wave', url, '#00000033', '#f50')

      wave.init()
    } else {
      if (wave1){
        wave1.destroy();
      }
      wave.reLoad(url)
      $('#play').attr('class', 'iconfont icon-play')
    }

    wave.finish(function() {
      $('#play').attr('class', 'iconfont icon-play')
    })
  }


  function playIn() {
    if (wave) {
      wave.playOrPause()
    }

    if (!wave.isPlaying) {
      // console.log(this)
      $(this).attr('class', 'iconfont icon-play')
    } else {
      $(this).attr('class', 'iconfont icon-pause')
    }
  }

  function playOut() {
    if (wave1) {
      wave1.playOrPause()
    }

    if (!wave1.isPlaying) {
      // console.log(this)
      $(this).attr('class', 'iconfont icon-play')
    } else {
      $(this).attr('class', 'iconfont icon-pause')
    }
  }

  function transformVocie() {
    if (wave1){
      wave1.destroy();
    }
    $('#out-wave>i').css('zIndex','10');
    $('#wave-transform-modal').removeClass('active');
    $.ajax({
      type: 'GET',
      url: `${baseUrl}/api/noises/${id}/denoise`,
      crossDomain: true,
      dataType: 'json',
      xhrFields: {
        'Access-Control-Allow-Origin': '*'
      },
      success: function(data) {
        $('#out-wave>i').css('zIndex','-1');
        $('#wave-transform-modal').addClass('active');
        // $('#wave-modal').addClass('active');
        var url = baseUrl + data
        addTransfrom(url)
      },
      error: function() {
      }
    })
  }

  function transformVocieFromAi(){

    if (wave1){
      wave1.destroy();
    }
    $('#out-wave>i').css('zIndex','10');
    $('#wave-transform-modal').removeClass('active');
    $.ajax({
      type: 'GET',
      url: `${baseUrl}/api/noises/${id}/transform`,
      crossDomain: true,
      dataType: 'json',
      xhrFields: {
        'Access-Control-Allow-Origin': '*'
      },
      success: function(data) {
        $('#out-wave>i').css('zIndex','-1');
        $('#wave-transform-modal').addClass('active');
        var url = baseUrl + data
        addTransfromAi(url)
      },
      error: function() {
        $('#out-wave>i').css('zIndex','-1');
        alert('失败了')
      }
    })
  }

  function getList() {
    // console.log(33);
    $.ajax({
      type: 'GET',
      url: `${baseUrl}/api/noises`,
      crossDomain: true,
      dataType: 'json',
      xhrFields: {
        'Access-Control-Allow-Origin': '*'
      },
      success: function(data) {
        // console.log(data);
        let str = ''

        for (let i = 0; i < data.length; i++) {
          str += `
          <p class="item" data-id="${data[i].id}" data-url="${
            data[i].raw_file
          }"><i class="iconfont icon-signal" />${timeToStr(data[i].timestamp)}</p>
        `
        }

        $('.sideBar').append(str)
        // $(this).addClass("done");
      },
      error: function() {}
    })
  }

  function addTransfrom(url) {
    if (!wave1) {
      wave1 = new CreateWave('#out-wave', url,'#00000033','#4cadfb')

      wave1.init()
    } else {
      wave1.reLoad(url,'#00000033','#4cadfb')
      $('#playOut').attr('class', 'iconfont icon-play')
    }

    wave1.finish(function() {
      $('#playOut').attr('class', 'iconfont icon-play')
    })
  }

  function addTransfromAi(url){
    if (!wave1) {
      wave1 = new CreateWave('#out-wave', url, '#00000033', '#000')

      wave1.init()
    } else {
      wave1.reLoad(url, '#00000033', '#000')
      $('#playOut').attr('class', 'iconfont icon-play')
    }

    wave1.finish(function() {
      $('#playOut').attr('class', 'iconfont icon-play')
    })
  }

  function timeToStr(str) {
    var num = str * 1000

    var time = new Date(num)

    var addZero = function(num) {
      return num < 10 ? '0' + num : num
    }

    var h = time.getHours()

    var m = time.getMinutes()

    var s = time.getSeconds()

    return `${addZero(h)}:${addZero(m)}:${addZero(s)}`
  }
}

function CreateWave(domStr, url, waveColor, progressColor) {
  this.domStr = domStr
  this.url = url
  this.waveColor = waveColor
  this.progressColor = progressColor
  this.Wave = null
  this.isPlaying = false
}

CreateWave.prototype = {
  constructor: CreateWave,
  init: function() {
    this.Wave = WaveSurfer.create({
      container: this.domStr,
      waveColor: this.waveColor,
      progressColor: this.progressColor,
      // audioRate:1.5,
      cursorColor: '#fff',
      barWidth: 2,
      height: 240
      // barWidth:1
    })

    this.load()
  },
  load() {
    this.Wave.load(this.url)
  },
  destroy() {
    this.Wave.destroy()
  },
  reLoad(url,waveColor,progressColor) {
    this.waveColor = waveColor
    this.progressColor = progressColor
    this.url = url
    this.destroy()
    this.init()
  },
  playOrPause() {
    this.Wave.playPause()
    this.isPlaying = this.Wave.isPlaying()
  },
  finish(fn) {
    this.Wave.on('finish', fn)
  }
}
