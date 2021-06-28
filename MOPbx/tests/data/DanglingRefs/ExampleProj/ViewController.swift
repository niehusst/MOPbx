//
//  ViewController.swift
//  ExampleProj
//

import UIKit

class ViewController: UITableViewController {

    var pics: [String] = []
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        DispatchQueue.global().async {
            // load images
            let fm = FileManager.default
            // assert nonnil OK bcus failure to read own app resources is crash-worthy
            let path = Bundle.main.resourcePath!
            let items = try! fm.contentsOfDirectory(atPath: path)
            
            self.pics.append(contentsOf: items.filter { item in
                item.hasPrefix("pic")
            })
            self.pics.sort()
        }
        
        // set our scene title
        title = "Best Image App"
    }
    
    
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return pics.count
    }

    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(
            withIdentifier: "Picture",
            for: indexPath)
        cell.textLabel?.text = pics[indexPath.row]
        return cell
    }
    
    override func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        guard
            let detail = storyboard?.instantiateViewController(
                withIdentifier: "Detail") as? DetailViewController
        else { return }
        
        // set image name
        detail.imageName = pics[indexPath.row]
        detail.imageIndex = indexPath.row
        detail.totalQuant = pics.count
        // nave to new vc
        navigationItem.backBarButtonItem = UIBarButtonItem(
                title: "Back",
                style: UIBarButtonItem.Style.plain,
                target: nil,
                action: nil)
        navigationController?.pushViewController(detail, animated: true)
        
    }
    
    @IBAction func shareButtonClicked(_ sender: Any) {
        /// ahsre the app?
        let shareVc = UIActivityViewController(activityItems: ["I fuking luv this app, ExampleProj, and u should downloand from <link>"], applicationActivities: nil)
        present(shareVc, animated: true)
    }
    
}
