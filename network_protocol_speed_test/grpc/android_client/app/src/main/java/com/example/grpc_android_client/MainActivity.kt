package com.example.grpc_android_client

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.TextView
import com.google.protobuf.ByteString
import com.squareup.okhttp.Dispatcher
import io.grpc.ConnectivityState
import io.grpc.ManagedChannel
import io.grpc.ManagedChannelBuilder

import io.grpc.examples.imageprocess.*
import io.grpc.stub.AbstractAsyncStub
import io.grpc.stub.ClientCallStreamObserver
import io.grpc.stub.StreamObserver
import java.io.InputStream
import java.lang.Exception

class MainActivity : AppCompatActivity() {
    val TAG = "MainActivity"
    private lateinit var channel : ManagedChannel
    private lateinit var stub : ImageProcessGrpc.ImageProcessBlockingStub
    private lateinit var textView : TextView
    private lateinit var imageByteString : ByteString

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        textView = this.findViewById<TextView>(R.id.textView)

        // Create channel
        channel = ManagedChannelBuilder.forTarget("192.168.32.104:8080")
            .keepAliveWithoutCalls(true)
            .usePlaintext()
            .build()

        // Create stub
        stub = ImageProcessGrpc.newBlockingStub(channel)

        channel.notifyWhenStateChanged(ConnectivityState.CONNECTING) { Log.d(TAG, "CONNECTING") }
        channel.notifyWhenStateChanged(ConnectivityState.TRANSIENT_FAILURE) { Log.d(TAG, "TRANSIENT_FAILURE") }
        channel.notifyWhenStateChanged(ConnectivityState.READY) { Log.d(TAG, "READY") }
        channel.notifyWhenStateChanged(ConnectivityState.IDLE) { Log.d(TAG, "IDLE") }
        channel.notifyWhenStateChanged(ConnectivityState.SHUTDOWN) { Log.d(TAG, "SHUTDOWN") }

        // Load testing image
//      var  imageFile = applicationContext.assets.open("112x112.jpg")
      var  imageFile = applicationContext.assets.open("224x224.jpg")
//        var imageFile = applicationContext.assets.open("640x640.jpg")
        imageByteString = ByteString.copyFrom(imageFile.readBytes())
        imageFile.close()
    }

    override fun onDestroy() {
        super.onDestroy()
        channel.shutdownNow()
    }

    fun testButtonClick(view: android.view.View) {
        val request = ImageProcessResquest.newBuilder()
            .setTimestamp(System.currentTimeMillis().toString())
            .setImage(imageByteString)
            .build()

        val response = stub.processImage(request)

        try {
            textView.text = (System.currentTimeMillis() - response.message.toLong()).toString() + " ms"
        } catch (e: Exception) {
            textView.text = e.message
        }
    }
}