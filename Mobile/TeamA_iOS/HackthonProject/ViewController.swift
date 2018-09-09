//
//  ViewController.swift
//  HackthonProject
//
//  Created by Doliant on 2018/9/8.
//  Copyright © 2018 Doliant. All rights reserved.
//

import UIKit
import Moya
import AVFoundation

class ViewController: UIViewController {
    
    @IBOutlet weak var playButton: UIButton!
    @IBOutlet weak var uploadButton: UIButton!
    @IBOutlet weak var endButton: UIButton!
    @IBOutlet weak var beginButton: UIButton!
    @IBOutlet weak var indicationView: UIView!
    
    private var audioSession: AVAudioSession?
    private var audioRecord: AVAudioRecorder?
    private var audioPlayer: AVAudioPlayer?
    private weak var timer: Timer?
    private let sandBoxPath = NSSearchPathForDirectoriesInDomains(.documentDirectory, .userDomainMask, true).last! + "/Audio/"
    private let fileName = "noise.wav"
    private var sourceURLPath: URL?
    
    
    // MARK: - Life Cycle
    override func viewDidLoad() {
        super.viewDidLoad()
        viewIntialization()
        sessionInitialization()
        recordInitialization()
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        timer?.invalidate()
        timer = nil
    }
}

// MARK: - AVAudioSession & AVRecord & AVAudioPlauyer initialization
extension ViewController {
    
    func viewIntialization() {
        uploadButton.isEnabled = false
        playButton.isEnabled = false
    }
    
    func timerIntialization() {
        let timer = Timer.scheduledTimer(timeInterval: 5.0, target: self, selector: #selector(timeExpiredAction), userInfo: nil
            , repeats: true)
        self.timer = timer
    }
    
    func sessionInitialization() {
        let audioSession = AVAudioSession.sharedInstance()
        _ = try? audioSession.setCategory(.playAndRecord, mode: .default, options: .defaultToSpeaker)
        _ = try? audioSession.setActive(true, options: .notifyOthersOnDeactivation)
        self.audioSession = audioSession
    }
    
    func recordInitialization() {
        
        if !FileManager.default.fileExists(atPath: sandBoxPath) {
           _ = try? FileManager.default.createDirectory(atPath: sandBoxPath, withIntermediateDirectories: false, attributes: nil)
        }
        
        sourceURLPath = URL(fileURLWithPath: sandBoxPath + fileName)
        
        var recordSetting = [String: Any]()
        /// 录音格式
        recordSetting[AVFormatIDKey] = kAudioFormatLinearPCM
        /// 采样率
        recordSetting[AVSampleRateKey] = 16000
        /// 声道
        recordSetting[AVNumberOfChannelsKey] = 1
        /// 采样点位数
        recordSetting[AVLinearPCMBitDepthKey] = 32
        /// 是否使用浮点数采样
        recordSetting[AVLinearPCMIsFloatKey] = true
        
        let audioRecord = try? AVAudioRecorder(url: sourceURLPath!, settings: recordSetting)
        audioRecord?.delegate = self
        audioRecord?.prepareToRecord()
        self.audioRecord = audioRecord
    }
    
    func playerInitialization()  {
        guard let sourceURLPath = sourceURLPath else {
            print("录音文件未存在")
            return
        }
        let audioPlayer = try? AVAudioPlayer(contentsOf: sourceURLPath)
        audioPlayer?.numberOfLoops = 0
        audioPlayer?.prepareToPlay()
        self.audioPlayer = audioPlayer
    }
}


// MARK: - AVRecordDelegate
extension ViewController: AVAudioRecorderDelegate {
    
    func audioRecorderDidFinishRecording(_ recorder: AVAudioRecorder, successfully flag: Bool) {
        print("录音完成准备上传")
        playerInitialization()
        indicationView.backgroundColor = .green
        uploadButton.isEnabled = true
        playButton.isEnabled = true
    }
    
}

// MARK: - Selector Method
extension ViewController {
    
    @objc func timeExpiredAction() {
        if audioRecord?.isRecording == true {
            audioRecord?.stop()
            indicationView.backgroundColor = .green
            timer?.fireDate = Date.distantFuture
        }
    }
    
    @IBAction func playButtonAction(_ sender: UIButton) {
        audioPlayer?.play()
    }
    
    @IBAction func beginButtonAction(_ sender: UIButton) {
        if audioRecord?.isRecording == false {
            audioRecord?.record()
            timerIntialization()
            indicationView.backgroundColor = .red
            sender.isEnabled = false
        }
    }
    
    @IBAction func endButtonAction(_ sender: UIButton) {
        if audioRecord?.isRecording == true {
            audioRecord?.stop()
            timer?.fireDate = Date.distantFuture
            indicationView.backgroundColor = .green
        }
    }
    
    @IBAction func uploadButtonAction(_ sender: UIButton) {
        let provider = MoyaProvider<AudioService>()
        provider.request(.upload(waveFile: sourceURLPath!)) { result in
            switch result {
            case .success(_):
                self.uploadButton.isEnabled  = false
                print("已经上传完成")
            case .failure(_):
                print("音频上传失败")
            }
        }
    }
    
    @IBAction func resetButtonAction(_ sender: UIButton) {
        beginButton.isEnabled = true
        uploadButton.isEnabled = false
        playButton.isEnabled = false
        indicationView.backgroundColor = .lightGray
        timer = nil
    }
    
}
