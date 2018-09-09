//
//  APIRouter.swift
//  HackthonProject
//
//  Created by Doliant on 2018/9/8.
//  Copyright © 2018 Doliant. All rights reserved.
//

import Foundation
import Moya

enum AudioService {
    case upload(waveFile: URL)
}

extension AudioService: TargetType {
    var baseURL: URL {
        return URL(fileURLWithPath: "http://192.168.15.112:60000/api")
    }
    
    var path: String {
        return "/noises"
    }
    
    var method: Moya.Method {
        return .post
    }
    
    var sampleData: Data {
        return Data(base64Encoded: "")!
    }
    
    var task: Task {
        switch self {
        case let .upload(waveFile):
            let uploadData = MultipartFormData(provider: .file(waveFile), name: "raw_file", fileName: "noise.wav", mimeType: "audio/wav")
            let multipartData = [uploadData]
            return .uploadMultipart(multipartData)
        }
    }
    
    var headers: [String : String]? {
        return nil
    }
    
    
}
