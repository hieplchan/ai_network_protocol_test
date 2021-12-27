package com.example.grpc_android_client

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.TextView
import com.squareup.okhttp.Dispatcher
import io.grpc.ConnectivityState
import io.grpc.ManagedChannel
import io.grpc.ManagedChannelBuilder

import io.grpc.examples.imageprocess.*
import io.grpc.stub.AbstractAsyncStub
import io.grpc.stub.ClientCallStreamObserver
import io.grpc.stub.StreamObserver
import java.lang.Exception

class MainActivity : AppCompatActivity() {
    val TAG = "MainActivity"
    private lateinit var channel : ManagedChannel
    private lateinit var stub : ImageProcessGrpc.ImageProcessBlockingStub
    private lateinit var textView : TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        textView = this.findViewById<TextView>(R.id.textView)

        // Create channel
        channel = ManagedChannelBuilder.forTarget("192.168.32.103:8080")
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

    }

    override fun onDestroy() {
        super.onDestroy()
        channel.shutdownNow()
    }

    fun testButtonClick(view: android.view.View) {
        val request = ImageProcessResquest.newBuilder()
            .setTimestamp("123456789")
            .build()

        val start = System.currentTimeMillis()

        val response = stub.processImage(request)

        val stop = System.currentTimeMillis()

        try {
            textView.text = response.message + " " + (stop - start).toString() + " ms"
        } catch (e: Exception) {
            textView.text = e.message
        }

    }
}