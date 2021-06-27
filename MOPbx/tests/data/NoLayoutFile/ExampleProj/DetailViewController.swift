//
//  DetailViewController.swift
//  ExampleProj
//

import UIKit

class DetailViewController: UIViewController {

    @IBOutlet var imageView: UIImageView!
    var imageName: String?
    var imageIndex: Int?
    var totalQuant: Int?
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        navigationController?.hidesBarsOnTap = true
    }
    
    override func viewDidLoad() { // onStart
        super.viewDidLoad()
        // load up that img
        if  let imageName = imageName,
            let imageIndex = imageIndex,
            let totalQuant = totalQuant {
            imageView.image = UIImage(named: imageName)
            title = "\(imageIndex+1) of \(totalQuant)"
        } else {
            title = "OOPS"
        }
        navigationItem.rightBarButtonItem = UIBarButtonItem(barButtonSystemItem: .action, target: self, action: #selector(shareTapped))
    }

    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        navigationController?.hidesBarsOnTap = false
    }
    
    @objc func shareTapped() {
        guard let image = imageView.image?.jpegData(compressionQuality: 0.8) else {
            print("no image foudn")
            return
        }
        
        let vc = UIActivityViewController(activityItems: [image, imageName!], applicationActivities: nil)
        vc.popoverPresentationController?.barButtonItem = navigationItem.rightBarButtonItem
        present(vc, animated: true)
    }

}
